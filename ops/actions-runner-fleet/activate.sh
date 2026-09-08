#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  cat <<'EOF'
Usage: activate.sh --host 10.230.50.LAST --name oe-rva23-qemu-LAST --enable-reviewed-policy [--allow-degraded]

Starts an already registered Runner only when the root-owned policy explicitly
enables enrollment and all host/Docker/QEMU/identity checks pass.
EOF
}

oe_reject_secret_arguments "$@"
enable_reviewed_policy=false
declare -a identity_arguments=()
while (($#)); do
  case $1 in
    --enable-reviewed-policy)
      enable_reviewed_policy=true
      shift
      ;;
    *)
      identity_arguments+=("$1")
      shift
      ;;
  esac
done
if ! oe_parse_host_name_args "${identity_arguments[@]}"; then usage; exit 0; fi
[[ $enable_reviewed_policy == true ]] || oe_usage_error 'activation requires --enable-reviewed-policy'
oe_require_root
oe_assert_local_host "$OE_ARG_HOST"
stage=$(oe_rollout_stage "$OE_ARG_HOST")
if [[ $OE_ARG_ALLOW_DEGRADED == true && $stage != conditional ]]; then
  oe_usage_error '--allow-degraded is restricted to the four audited conditional hosts'
fi
oe_assert_platform "$OE_ARG_ALLOW_DEGRADED"
oe_load_identity
[[ $OE_IDENTITY_HOST == "$OE_ARG_HOST" && $OE_IDENTITY_NAME == "$OE_ARG_NAME" ]] || oe_die 'installed identity does not match arguments'
[[ $OE_IDENTITY_ALLOW_DEGRADED == "$OE_ARG_ALLOW_DEGRADED" ]] \
  || oe_die 'activation --allow-degraded must exactly match the installed identity policy'
oe_load_policy
oe_check_no_other_runners "$OE_ARG_NAME"

runner_dir=$(oe_runner_dir "$OE_ARG_NAME")
[[ -r $runner_dir/.runner && -r $runner_dir/.credentials ]] || oe_die 'register.sh must complete before activation'
service=$(oe_service_name "$OE_ARG_NAME")
oe_load_cleanup_image_lock "$oe_runner_config/cleanup-image.lock"
if ! oe_run docker image inspect "$CLEANUP_IMAGE_REF" >/dev/null 2>&1; then
  timeout --signal=KILL 20m docker pull --quiet "$CLEANUP_IMAGE_REF" >/dev/null
fi
oe_run docker image inspect "$CLEANUP_IMAGE_REF" >/dev/null 2>&1 \
  || oe_die 'digest-locked cleanup image is unavailable after activation cache preparation'
"$oe_runner_libexec/cleanup.sh" --name "$OE_ARG_NAME" --phase before

policy_changed=false
activation_complete=false
temporary_policy=
rollback_activation() {
  local status=$?
  if [[ $activation_complete == false ]]; then
    set +e
    oe_systemctl disable --now "$service" >/dev/null 2>&1
    [[ -z $temporary_policy ]] || rm -f -- "$temporary_policy"
    if [[ $policy_changed == true ]]; then
      rollback_policy=$(mktemp "$oe_runner_config/.policy.conf.rollback.XXXXXX")
      awk '
        /^OE_RUNNER_ENROLLMENT_ENABLED=true$/ {print "OE_RUNNER_ENROLLMENT_ENABLED=false"; changed=1; next}
        {print}
        END {if (changed != 1) exit 1}
      ' "$oe_runner_config/policy.conf" >"$rollback_policy"
      rollback_status=$?
      if [[ $rollback_status -eq 0 ]]; then
        chown root:root "$rollback_policy"
        chmod 0644 "$rollback_policy"
        mv -f -- "$rollback_policy" "$oe_runner_config/policy.conf"
        printf 'Activation failed; service was stopped and enrollment policy was restored to false.\n' >&2
      else
        rm -f -- "$rollback_policy"
        printf 'CRITICAL: activation failed and enrollment policy rollback also failed; service was stopped.\n' >&2
      fi
    fi
    set -e
  fi
  exit "$status"
}
trap rollback_activation EXIT

if [[ $OE_POLICY_ENROLLMENT_ENABLED == false ]]; then
  temporary_policy=$(mktemp "$oe_runner_config/.policy.conf.XXXXXX")
  awk '
    /^OE_RUNNER_ENROLLMENT_ENABLED=false$/ {print "OE_RUNNER_ENROLLMENT_ENABLED=true"; changed=1; next}
    {print}
    END {if (changed != 1) exit 1}
  ' "$oe_runner_config/policy.conf" >"$temporary_policy" \
    || oe_die 'policy could not be atomically enabled'
  chown root:root "$temporary_policy"
  chmod 0644 "$temporary_policy"
  policy_changed=true
  mv -f -- "$temporary_policy" "$oe_runner_config/policy.conf"
  temporary_policy=
  oe_load_policy
fi
[[ $OE_POLICY_ENROLLMENT_ENABLED == true ]] || oe_die 'activation policy is not enabled'
"$oe_runner_libexec/preflight.sh" --name "$OE_ARG_NAME"
oe_systemctl enable --now "$service"
oe_systemctl --quiet is-active "$service" || oe_die 'Runner service did not become active'
activation_complete=true
trap - EXIT
printf 'Activated %s on %s (%s stage).\n' "$OE_ARG_NAME" "$OE_ARG_HOST" "$stage"
