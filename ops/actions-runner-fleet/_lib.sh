#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# shellcheck disable=SC2034

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then
  printf '_lib.sh must be sourced, not executed\n' >&2
  exit 64
fi

set -Eeuo pipefail
set +x
# This file is sourced by multiple entry points; these shared assignments are
# intentionally consumed by the caller rather than by every source operation.
oe_runner_base=/opt/openeuler-actions-runner
oe_runner_lock_dir=$oe_runner_base/.locks
oe_runner_user=oegha
oe_runner_group=oegha
oe_runner_repo_url=https://github.com/yinjiayi/openeuler-riscv-packages
oe_runner_repo_slug=yinjiayi/openeuler-riscv-packages
oe_runner_libexec=/usr/local/libexec/openeuler-actions-runner
oe_runner_config=/etc/openeuler-actions-runner
oe_systemctl_path=/usr/bin/systemctl

oe_run() {
  "$@"
}

oe_die() {
  printf 'runner-fleet: %s\n' "$*" >&2
  exit 1
}

oe_usage_error() {
  printf 'runner-fleet: %s\n' "$*" >&2
  exit 64
}

oe_require_root() {
  [[ $EUID -eq 0 ]] || oe_die 'this operation must run as root'
}

oe_assert_systemctl_integrity() {
  local owner package_record package status version extra verification

  [[ -f $oe_systemctl_path && ! -L $oe_systemctl_path && -x $oe_systemctl_path ]] \
    || oe_die 'systemctl is missing, linked, or not a regular executable'
  [[ $(stat -c '%U:%G:%a' "$oe_systemctl_path" 2>/dev/null) == root:root:755 ]] \
    || oe_die 'systemctl ownership or mode differs from the Ubuntu package contract'
  owner=$(dpkg-query --search "$oe_systemctl_path" 2>/dev/null) \
    || oe_die 'systemctl has no dpkg owner'
  [[ $owner == 'systemd: /usr/bin/systemctl' ]] \
    || oe_die 'systemctl dpkg ownership differs from the Ubuntu package contract'
  package_record=$(dpkg-query --show \
    --showformat='${binary:Package}\t${Status}\t${Version}\n' systemd 2>/dev/null) \
    || oe_die 'systemd package metadata is unavailable'
  IFS=$'\t' read -r package status version extra <<<"$package_record"
  [[ $package == systemd && $status == 'install ok installed' && -z $extra \
    && $version =~ ^[0-9][0-9A-Za-z.+:~_-]*$ ]] \
    || oe_die 'systemd package name, status, or version is invalid'
  if ! verification=$(dpkg --verify systemd 2>&1); then
    oe_die 'systemd package integrity verification could not complete'
  fi
  [[ -z $verification ]] \
    || oe_die 'systemd package files differ from the installed package database'
}

oe_systemctl() {
  oe_assert_systemctl_integrity
  oe_run "$oe_systemctl_path" --no-pager "$@"
}

oe_reject_secret_arguments() {
  local argument
  for argument in "$@"; do
    case "$argument" in
      --token|--token=*|--pat|--pat=*|--jitconfig|--jitconfig=*|ghp_*|gho_*|ghu_*|ghs_*|ghr_*|github_pat_*)
        oe_usage_error 'credentials are forbidden in command arguments; use stdin or the documented process environment variable'
        ;;
    esac
  done
}

oe_validate_host_name() {
  local host=${1:?host is required}
  local name=${2:?name is required}
  local last
  [[ $host =~ ^10\.230\.50\.([0-9]{3})$ ]] || oe_usage_error "host is outside 10.230.50.201-10.230.50.250: $host"
  last=${BASH_REMATCH[1]}
  (( 10#$last >= 201 && 10#$last <= 250 )) || oe_usage_error "host is outside 10.230.50.201-10.230.50.250: $host"
  [[ $name == "oe-rva23-qemu-$((10#$last))" ]] || oe_usage_error "runner name must be oe-rva23-qemu-$((10#$last)) for $host"
}

oe_host_from_name() {
  local name=${1:?name is required}
  local last
  [[ $name =~ ^oe-rva23-qemu-([0-9]{3})$ ]] || oe_usage_error "invalid runner name: $name"
  last=${BASH_REMATCH[1]}
  (( 10#$last >= 201 && 10#$last <= 250 )) || oe_usage_error "runner name is outside the fleet: $name"
  printf '10.230.50.%d\n' "$((10#$last))"
}

oe_rollout_stage() {
  local host=${1:?host is required}
  local last=${host##*.}
  case $last in
    201|202|203|204|205) printf 'canary\n' ;;
    211|220|224|231) printf 'conditional\n' ;;
    *) printf 'clean-expansion\n' ;;
  esac
}

oe_assert_local_host() {
  local expected=${1:?expected host is required}
  oe_run ip -o -4 address show scope global 2>/dev/null \
    | awk '{split($4, address, "/"); print address[1]}' \
    | grep -Fxq -- "$expected" \
    || oe_die "this machine does not own expected address $expected"
}

oe_assert_platform() {
  local allow_degraded=${1:-false}
  local state
  oe_assert_systemctl_integrity
  [[ $(uname -m) == x86_64 ]] || oe_die 'runner host must be x86_64'
  # shellcheck disable=SC1091
  source /etc/os-release
  [[ ${ID:-} == ubuntu && ${VERSION_ID:-} == 26.04 ]] \
    || oe_die "runner host must be Ubuntu 26.04; observed ${ID:-unknown} ${VERSION_ID:-unknown}"
  state=$(oe_systemctl is-system-running 2>/dev/null || true)
  case $state in
    running) ;;
    degraded)
      [[ $allow_degraded == true ]] || oe_die 'systemd is degraded; conditional hosts require a separate reviewed rollout'
      ;;
    *) oe_die "systemd is not operational: ${state:-unknown}" ;;
  esac
}

oe_runner_dir() {
  local name=${1:?name is required}
  oe_host_from_name "$name" >/dev/null
  printf '%s/%s\n' "$oe_runner_base" "$name"
}

oe_job_workspace() {
  local work_dir=${1:?Runner work directory is required}
  local presented=${2:?job workspace is required}
  local repository_name expected parent
  [[ -d $work_dir && ! -L $work_dir ]] || oe_die 'Runner work directory is missing or unsafe'
  repository_name=${oe_runner_repo_slug#*/}
  [[ $oe_runner_repo_slug == */* && -n $repository_name && $repository_name != */* ]] \
    || oe_die 'configured repository slug is invalid'
  parent=$work_dir/$repository_name
  expected=$parent/$repository_name
  [[ $presented == "$expected" ]] || oe_die 'job hook working directory is outside the configured repository workspace'
  [[ -d $parent && ! -L $parent && -d $expected && ! -L $expected ]] \
    || oe_die 'job workspace or its repository parent is missing or unsafe'
  printf '%s\n' "$expected"
}

oe_runner_version() {
  local runner=${1:?Runner.Listener path is required}
  local working_directory=${2:?Runner working directory is required}
  [[ -x $runner && ! -L $runner ]] || oe_die "Runner.Listener is missing or unsafe: $runner"
  [[ -d $working_directory && ! -L $working_directory ]] \
    || oe_die "Runner working directory is missing or unsafe: $working_directory"
  if [[ $EUID -eq 0 ]]; then
    # Runner.Listener always opens a timestamped _diag log, even for
    # --version. Lifecycle commands run as root immediately before systemd's
    # oegha preflight, so probing as root can create a same-second root-owned
    # log that the service account cannot reopen. Use the service identity for
    # every installed-payload probe; extracted payloads are handled separately
    # before the account-owned runtime tree exists.
    # Positional parameters intentionally expand in the child shell.
    # shellcheck disable=SC2016
    runuser --user "$oe_runner_user" -- /bin/bash -c \
      'cd -- "${1:?}" && exec "${2:?}" --version' bash "$working_directory" "$runner"
  else
    (cd -- "$working_directory" && "$runner" --version)
  fi
}

oe_service_name() {
  local name=${1:?name is required}
  oe_host_from_name "$name" >/dev/null
  printf 'openeuler-actions-runner@%s.service\n' "$name"
}

oe_load_identity() {
  local identity=$oe_runner_config/identity.conf
  local key value
  OE_IDENTITY_HOST=
  OE_IDENTITY_NAME=
  OE_IDENTITY_ALLOW_DEGRADED=
  [[ -f $identity && ! -L $identity && -r $identity ]] || oe_die "identity file is missing or unsafe: $identity"
  [[ $(stat -c '%U:%G:%a' "$identity") == root:root:644 ]] || oe_die 'identity file ownership/mode is unsafe'
  while IFS='=' read -r key value; do
    case $key in
      HOST_IP) OE_IDENTITY_HOST=$value ;;
      RUNNER_NAME) OE_IDENTITY_NAME=$value ;;
      ALLOW_DEGRADED) OE_IDENTITY_ALLOW_DEGRADED=$value ;;
      ''|'#'*) ;;
      *) oe_die "unexpected identity key: $key" ;;
    esac
  done <"$identity"
  oe_validate_host_name "$OE_IDENTITY_HOST" "$OE_IDENTITY_NAME"
  [[ $OE_IDENTITY_ALLOW_DEGRADED == true || $OE_IDENTITY_ALLOW_DEGRADED == false ]] \
    || oe_die 'identity degraded-host policy is invalid'
  if [[ $OE_IDENTITY_ALLOW_DEGRADED == true ]]; then
    [[ $(oe_rollout_stage "$OE_IDENTITY_HOST") == conditional ]] \
      || oe_die 'degraded-host permission is restricted to the four conditional hosts'
  fi
}

oe_parse_host_name_args() {
  OE_ARG_HOST=
  OE_ARG_NAME=
  OE_ARG_ALLOW_DEGRADED=false
  while (($#)); do
    case $1 in
      --host)
        (($# >= 2)) || oe_usage_error '--host needs a value'
        OE_ARG_HOST=$2
        shift 2
        ;;
      --name)
        (($# >= 2)) || oe_usage_error '--name needs a value'
        OE_ARG_NAME=$2
        shift 2
        ;;
      --allow-degraded)
        OE_ARG_ALLOW_DEGRADED=true
        shift
        ;;
      -h|--help)
        return 2
        ;;
      *) oe_usage_error "unknown argument: $1" ;;
    esac
  done
  [[ -n $OE_ARG_HOST && -n $OE_ARG_NAME ]] || oe_usage_error '--host and --name are required'
  oe_validate_host_name "$OE_ARG_HOST" "$OE_ARG_NAME"
}

oe_load_policy() {
  local policy=$oe_runner_config/policy.conf
  local key value
  OE_POLICY_ENROLLMENT_ENABLED=
  OE_POLICY_REPOSITORY=
  OE_POLICY_REF=
  OE_POLICY_WORKFLOW_REFS=
  OE_POLICY_EVENTS=
  [[ -f $policy && ! -L $policy && -r $policy ]] || oe_die "policy file is missing or unsafe: $policy"
  [[ $(stat -c '%U:%G:%a' "$policy") == root:root:644 ]] || oe_die 'policy file ownership/mode is unsafe'
  while IFS='=' read -r key value; do
    case $key in
      OE_RUNNER_ENROLLMENT_ENABLED) OE_POLICY_ENROLLMENT_ENABLED=$value ;;
      OE_RUNNER_ALLOWED_REPOSITORY) OE_POLICY_REPOSITORY=$value ;;
      OE_RUNNER_ALLOWED_REF) OE_POLICY_REF=$value ;;
      OE_RUNNER_ALLOWED_WORKFLOW_REFS) OE_POLICY_WORKFLOW_REFS=$value ;;
      OE_RUNNER_ALLOWED_EVENTS) OE_POLICY_EVENTS=$value ;;
      ''|'#'*) ;;
      *) oe_die "unexpected policy key: $key" ;;
    esac
  done <"$policy"
  [[ $OE_POLICY_ENROLLMENT_ENABLED == true || $OE_POLICY_ENROLLMENT_ENABLED == false ]] || oe_die 'policy enrollment flag is invalid'
  [[ $OE_POLICY_REPOSITORY == "$oe_runner_repo_slug" ]] || oe_die 'policy repository is invalid'
  [[ $OE_POLICY_REF == refs/heads/main ]] || oe_die 'policy ref must be protected main'
  [[ $OE_POLICY_WORKFLOW_REFS == "$oe_runner_repo_slug/.github/workflows/package-ci.yml@refs/heads/main,$oe_runner_repo_slug/.github/workflows/rpm-repo-backfill.yml@refs/heads/main" ]] \
    || oe_die 'policy workflow refs are invalid or out of canonical order'
  [[ $OE_POLICY_EVENTS == push,workflow_dispatch ]] || oe_die 'policy events are invalid'
}

oe_load_release_lock() {
  local lock=${1:?release lock path is required}
  local key value
  RUNNER_VERSION=
  RUNNER_ARCHIVE=
  RUNNER_URL=
  RUNNER_SHA256=
  RUNNER_SIZE=
  [[ -r $lock ]] || oe_die "release lock is missing: $lock"
  while IFS='=' read -r key value; do
    case $key in
      RUNNER_VERSION) RUNNER_VERSION=$value ;;
      RUNNER_ARCHIVE) RUNNER_ARCHIVE=$value ;;
      RUNNER_URL) RUNNER_URL=$value ;;
      RUNNER_SHA256) RUNNER_SHA256=$value ;;
      RUNNER_SIZE) RUNNER_SIZE=$value ;;
      ''|'#'*) ;;
      *) oe_die "unexpected release lock key: $key" ;;
    esac
  done <"$lock"
  [[ $RUNNER_VERSION == 2.336.0 ]] || oe_die 'release lock version is not approved'
  [[ $RUNNER_ARCHIVE == actions-runner-linux-x64-2.336.0.tar.gz ]] || oe_die 'release lock archive is not approved'
  [[ $RUNNER_URL == https://github.com/actions/runner/releases/download/v2.336.0/actions-runner-linux-x64-2.336.0.tar.gz ]] \
    || oe_die 'release lock URL is not approved'
  [[ $RUNNER_SHA256 == 04cf0be1aff4c3ec3554466c39124ca250e3effd8873bb7e8d68535aa9505d5d ]] \
    || oe_die 'release lock SHA-256 is not approved'
  [[ $RUNNER_SIZE == 226035903 ]] || oe_die 'release lock size is not approved'
}

oe_load_cleanup_image_lock() {
  local lock=${1:?cleanup image lock path is required}
  local key value
  CLEANUP_IMAGE_REF=
  [[ -f $lock && ! -L $lock && -r $lock ]] || oe_die "cleanup image lock is missing or unsafe: $lock"
  while IFS='=' read -r key value; do
    case $key in
      CLEANUP_IMAGE_REF) CLEANUP_IMAGE_REF=$value ;;
      ''|'#'*) ;;
      *) oe_die "unexpected cleanup image lock key: $key" ;;
    esac
  done <"$lock"
  [[ $CLEANUP_IMAGE_REF =~ ^ghcr\.io/yinjiayi/openeuler-riscv64-rpmbuild@sha256:[0-9a-f]{64}$ ]] \
    || oe_die 'cleanup image lock is invalid'
}

oe_install_identity() {
  local host=${1:?host is required}
  local name=${2:?name is required}
  local allow_degraded=${3:?degraded-host policy is required}
  local temporary
  [[ $allow_degraded == true || $allow_degraded == false ]] || oe_die 'invalid degraded-host policy'
  if [[ $allow_degraded == true ]]; then
    [[ $(oe_rollout_stage "$host") == conditional ]] \
      || oe_die 'degraded-host permission is restricted to the four conditional hosts'
  fi
  install -d -o root -g root -m 0755 "$oe_runner_config"
  if [[ -e $oe_runner_config/identity.conf ]]; then
    oe_load_identity
    [[ $OE_IDENTITY_HOST == "$host" && $OE_IDENTITY_NAME == "$name" && $OE_IDENTITY_ALLOW_DEGRADED == "$allow_degraded" ]] \
      || oe_die 'existing identity differs; uninstall explicitly before changing host policy'
    return
  fi
  temporary=$(mktemp "$oe_runner_config/.identity.conf.XXXXXX")
  printf 'HOST_IP=%s\nRUNNER_NAME=%s\nALLOW_DEGRADED=%s\n' \
    "$host" "$name" "$allow_degraded" >"$temporary"
  chown root:root "$temporary"
  chmod 0644 "$temporary"
  mv -f -- "$temporary" "$oe_runner_config/identity.conf"
}

oe_read_secret() {
  local env_name=${1:?environment variable name is required}
  local prompt=${2:?prompt is required}
  local secret=
  if [[ -n ${!env_name-} ]]; then
    secret=${!env_name}
    unset "$env_name"
  elif [[ -t 0 ]]; then
    IFS= read -r -s -p "$prompt" secret
    printf '\n' >&2
  else
    IFS= read -r secret || oe_die 'credential input ended before one line was read'
  fi
  [[ -n $secret ]] || oe_die 'credential is empty'
  [[ ${#secret} -le 512 ]] || oe_die 'credential is too long'
  [[ $secret != *$'\n'* && $secret != *$'\r'* ]] || oe_die 'credential contains a line break'
  case $secret in
    ghp_*|gho_*|ghu_*|ghs_*|ghr_*|github_pat_*)
      oe_die 'a long-lived GitHub access token is not a runner registration/removal token'
      ;;
  esac
  OE_READ_SECRET=$secret
}

oe_wipe_secret() {
  OE_READ_SECRET=
  unset OE_READ_SECRET
}

oe_check_no_other_runners() {
  local name=${1:?name is required}
  local unit directory runner_dir
  runner_dir=$(oe_runner_dir "$name")
  while IFS= read -r unit; do
    case $unit in
      ''|openeuler-actions-runner@.service|"$(oe_service_name "$name")") ;;
      *) oe_die "another Actions Runner service already exists: $unit" ;;
    esac
  done < <(oe_systemctl list-unit-files --type=service --no-legend 'actions.runner*' 'openeuler-actions-runner@*' 2>/dev/null | awk '{print $1}')
  if [[ -d $oe_runner_base ]]; then
    while IFS= read -r directory; do
      case $directory in
        "$runner_dir"|"$oe_runner_lock_dir") ;;
        *) oe_die "another runner directory exists: $directory" ;;
      esac
    done < <(find "$oe_runner_base" -mindepth 1 -maxdepth 1 -type d -print)
  fi
}
