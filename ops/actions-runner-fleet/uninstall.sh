#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  cat <<'EOF'
Usage: uninstall.sh --host 10.230.50.LAST --name oe-rva23-qemu-LAST [--allow-degraded]

If the Runner is registered, reads one short-lived removal token from stdin or
OE_RUNNER_REMOVAL_TOKEN. It never accepts a credential argument. Package
removal is intentionally out of scope because Docker/QEMU may be shared host
dependencies.
EOF
}

oe_reject_secret_arguments "$@"
if ! oe_parse_host_name_args "$@"; then usage; exit 0; fi
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
  || oe_die 'uninstall --allow-degraded must exactly match the installed identity policy'

runner_dir=$(oe_runner_dir "$OE_ARG_NAME")
service=$(oe_service_name "$OE_ARG_NAME")
oe_systemctl disable --now "$service" >/dev/null 2>&1 || true
if [[ -r $runner_dir/.runner ]]; then
  [[ -x $runner_dir/config.sh ]] || oe_die 'registered Runner is missing config.sh'
  oe_read_secret OE_RUNNER_REMOVAL_TOKEN 'Short-lived Runner removal token: '
  trap 'oe_wipe_secret; chown root:root "$runner_dir" 2>/dev/null || true' EXIT
  chown "$oe_runner_user:$oe_runner_group" "$runner_dir"
  printf '%s\n' "$OE_READ_SECRET" \
    | "$oe_runner_libexec/credential_exec.py" remove --user "$oe_runner_user" --name "$OE_ARG_NAME"
  oe_wipe_secret
  chown root:root "$runner_dir"
  trap - EXIT
  [[ ! -e $runner_dir/.runner ]] || oe_die 'Runner removal did not clear local registration'
fi

if [[ -d $runner_dir ]]; then
  [[ ! -L $runner_dir && $runner_dir == "$oe_runner_base/$OE_ARG_NAME" ]] || oe_die 'runner directory is unsafe'
  find "$runner_dir" -mindepth 1 -xdev -delete
  rmdir -- "$runner_dir"
fi
rm -f -- "$oe_runner_config/identity.conf"
oe_systemctl daemon-reload
printf 'Uninstalled %s from %s. Docker/QEMU packages were retained.\n' "$OE_ARG_NAME" "$OE_ARG_HOST"
