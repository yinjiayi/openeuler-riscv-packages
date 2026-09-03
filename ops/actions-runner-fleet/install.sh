#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  cat <<'EOF'
Usage: install.sh --host 10.230.50.LAST --name oe-rva23-qemu-LAST [--allow-degraded]

Installs the pinned Runner payload, Docker, RISC-V QEMU/binfmt, root-owned
policy/hooks, and a disabled systemd unit. It does not register or start the
Actions Runner and accepts no credential.
EOF
}

oe_reject_secret_arguments "$@"
if ! oe_parse_host_name_args "$@"; then
  usage
  exit 0
fi
oe_require_root
oe_assert_local_host "$OE_ARG_HOST"
stage=$(oe_rollout_stage "$OE_ARG_HOST")
if [[ $OE_ARG_ALLOW_DEGRADED == true && $stage != conditional ]]; then
  oe_usage_error '--allow-degraded is restricted to the four audited conditional hosts'
fi
oe_assert_platform "$OE_ARG_ALLOW_DEGRADED"
oe_load_release_lock "$source_dir/runner-release.lock"

cpu_count=$(nproc)
memory_bytes=$(awk '/^MemTotal:/ {print $2 * 1024}' /proc/meminfo)
opt_available=$(df --output=avail --block-size=1 /opt | awk 'NR == 2 {print $1}')
(( cpu_count >= 16 )) || oe_die "host exposes fewer than 16 CPUs: $cpu_count"
awk -v value="$memory_bytes" 'BEGIN {exit !(value >= 32 * 1024 * 1024 * 1024)}' \
  || oe_die 'host has less than 32 GiB RAM'
(( opt_available >= 200 * 1024 * 1024 * 1024 )) || oe_die 'host has less than 200 GiB free beneath /opt'

for endpoint in \
  https://github.com/ \
  https://api.github.com/ \
  https://codeload.github.com/ \
  https://objects.githubusercontent.com/ \
  https://results-receiver.actions.githubusercontent.com/ \
  https://ghcr.io/v2/ \
  https://repo.openeuler.org/openEuler-24.03-LTS-SP3/everything/riscv64/rva23/riscv64/; do
  curl --silent --show-error --location --output /dev/null \
    --connect-timeout 5 --max-time 20 --retry 2 --retry-delay 1 --retry-all-errors \
    --write-out '%{http_code}' \
    "$endpoint" \
    | grep -Eq '^(2|3|4)[0-9]{2}$' \
    || oe_die "required HTTPS endpoint is unreachable: $endpoint"
done

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
  ca-certificates curl docker.io git iptables jq qemu-user qemu-user-binfmt rsync tar xz-utils
oe_assert_systemctl_integrity
update-alternatives --auto iptables
[[ -L /usr/sbin/iptables \
  && $(readlink -- /usr/sbin/iptables) == /etc/alternatives/iptables \
  && -x /usr/sbin/iptables ]] \
  || oe_die 'Docker firewall helper is missing after installation: /usr/sbin/iptables'
/usr/sbin/iptables --version >/dev/null \
  || oe_die 'Docker firewall helper does not execute after installation'

if ! getent passwd "$oe_runner_user" >/dev/null; then
  useradd --system --user-group --home-dir /var/lib/oegha --create-home --shell /usr/sbin/nologin "$oe_runner_user"
fi
account=$(getent passwd "$oe_runner_user")
IFS=: read -r account_name _ account_uid _ _ account_home account_shell <<<"$account"
[[ $account_name == "$oe_runner_user" && $account_uid -ne 0 && $account_home == /var/lib/oegha && $account_shell == /usr/sbin/nologin ]] \
  || oe_die 'existing oegha account does not match the managed system account'
getent group docker >/dev/null || oe_die 'docker group was not created by the package'
usermod --append --groups docker "$oe_runner_user"
passwd --lock "$oe_runner_user" >/dev/null 2>&1 || true

if [[ -e $oe_runner_lock_dir || -L $oe_runner_lock_dir ]]; then
  [[ -d $oe_runner_lock_dir && ! -L $oe_runner_lock_dir ]] \
    || oe_die 'managed cleanup lock directory is not a real directory'
fi
install -d -o root -g root -m 0755 \
  "$oe_runner_base" "$oe_runner_lock_dir" "$oe_runner_libexec" "$oe_runner_config"
[[ $(stat -c '%U:%G:%a' "$oe_runner_lock_dir") == root:root:755 ]] \
  || oe_die 'managed cleanup lock directory ownership/mode is unsafe'
install -o root -g root -m 0755 \
  "$source_dir/_lib.sh" \
  "$source_dir/audit.sh" \
  "$source_dir/preflight.sh" \
  "$source_dir/job-guard.sh" \
  "$source_dir/cleanup.sh" \
  "$source_dir/docker-cleanup.py" \
  "$source_dir/job-started.sh" \
  "$source_dir/job-completed.sh" \
  "$oe_runner_libexec/"
install -o root -g root -m 0755 "$source_dir/credential_exec.py" "$oe_runner_libexec/credential_exec.py"
if [[ -e $oe_runner_config/policy.conf ]]; then
  # An idempotent reinstall must not turn an activated host back into the
  # disabled state while its service is still running.
  oe_load_policy
else
  install -o root -g root -m 0644 "$source_dir/policy.conf" "$oe_runner_config/policy.conf"
fi
install -o root -g root -m 0644 "$source_dir/runner-release.lock" "$oe_runner_config/runner-release.lock"
install -o root -g root -m 0644 "$source_dir/cleanup-image.lock" "$oe_runner_config/cleanup-image.lock"
install -o root -g root -m 0644 "$source_dir/openeuler-actions-runner@.service" /etc/systemd/system/openeuler-actions-runner@.service
oe_install_identity "$OE_ARG_HOST" "$OE_ARG_NAME" "$OE_ARG_ALLOW_DEGRADED"

runner_dir=$(oe_runner_dir "$OE_ARG_NAME")
installed=false
if [[ -x $runner_dir/bin/Runner.Listener && -r $runner_dir/.release ]]; then
  observed_version=$(oe_runner_version "$runner_dir/bin/Runner.Listener" "$runner_dir")
  if [[ $observed_version == "$RUNNER_VERSION" ]] && grep -Fxq "sha256=$RUNNER_SHA256" "$runner_dir/.release"; then
    installed=true
  else
    oe_die 'a different or unverifiable Runner payload exists; uninstall it explicitly before replacement'
  fi
elif [[ -e $runner_dir ]]; then
  oe_die "unmanaged or partial runner directory already exists: $runner_dir"
fi

if [[ $installed == false ]]; then
  install_root=$(mktemp -d "$oe_runner_base/.install-${OE_ARG_NAME}.XXXXXX")
  trap 'rm -rf -- "$install_root"' EXIT
  archive=$install_root/$RUNNER_ARCHIVE
  payload=$install_root/payload
  install -d -o root -g root -m 0755 "$payload"
  curl --fail --silent --show-error --location --output "$archive" \
    --connect-timeout 10 --max-time 300 --retry 3 --retry-delay 2 --retry-all-errors \
    "$RUNNER_URL"
  [[ $(stat -c '%s' "$archive") == "$RUNNER_SIZE" ]] \
    || oe_die 'Runner archive size does not match the lock'
  printf '%s  %s\n' "$RUNNER_SHA256" "$archive" | sha256sum --check --status \
    || oe_die 'Runner archive SHA-256 does not match the lock'
  while IFS= read -r member; do
    normalized=${member#./}
    [[ -z $normalized || $normalized == . ]] && continue
    [[ $normalized != /* && $normalized != ../* && $normalized != */../* && $normalized != *'/..' ]] \
      || oe_die "Runner archive contains an unsafe path: $member"
  done < <(tar --list --gzip --file "$archive")
  tar --extract --gzip --file "$archive" --directory "$payload" --no-same-owner
  [[ -x $payload/bin/Runner.Listener && ! -L $payload/bin/Runner.Listener ]] || oe_die 'Runner.Listener is missing or unsafe'
  [[ -x $payload/config.sh && ! -L $payload/config.sh ]] || oe_die 'config.sh is missing or unsafe'
  [[ $("$payload/bin/Runner.Listener" --version) == "$RUNNER_VERSION" ]] || oe_die 'extracted Runner version is not the lock version'
  printf 'version=%s\narchive=%s\nsha256=%s\nsize=%s\n' \
    "$RUNNER_VERSION" "$RUNNER_ARCHIVE" "$RUNNER_SHA256" "$RUNNER_SIZE" >"$payload/.release"
  chown -R root:root "$payload"
  mv -- "$payload" "$runner_dir"
  rm -rf -- "$install_root"
  trap - EXIT
fi

install -d -o "$oe_runner_user" -g "$oe_runner_group" -m 0700 \
  "$runner_dir/_work" "$runner_dir/_diag" "$runner_dir/_state" \
  "$runner_dir/_state/home" "$runner_dir/_state/docker" "$runner_dir/_state/baseline"
cleanup_lock=$oe_runner_lock_dir/$OE_ARG_NAME.lock
if [[ -e $cleanup_lock || -L $cleanup_lock ]]; then
  [[ -f $cleanup_lock && ! -L $cleanup_lock ]] || oe_die 'managed cleanup lock is not a regular file'
  chown root:"$oe_runner_group" "$cleanup_lock"
  chmod 0660 "$cleanup_lock"
else
  install -o root -g "$oe_runner_group" -m 0660 /dev/null "$cleanup_lock"
fi
chown root:root "$runner_dir"
chmod 0755 "$runner_dir"
oe_check_no_other_runners "$OE_ARG_NAME"

oe_systemctl daemon-reload
oe_systemctl enable --now docker.service
oe_systemctl restart systemd-binfmt.service
runuser --user "$oe_runner_user" -- docker info >/dev/null
command -v qemu-riscv64 >/dev/null || oe_die 'qemu-riscv64 is missing after installation'
[[ -r /proc/sys/fs/binfmt_misc/qemu-riscv64 ]] || oe_die 'qemu-riscv64 binfmt registration is absent after installation'
grep -Fxq enabled /proc/sys/fs/binfmt_misc/qemu-riscv64 || oe_die 'qemu-riscv64 binfmt registration is not enabled'

printf 'Installed %s on %s (%s stage). Enrollment remains disabled; register.sh is the separate offline enrollment step.\n' \
  "$OE_ARG_NAME" "$OE_ARG_HOST" "$stage"
