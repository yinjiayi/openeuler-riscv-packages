#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  cat <<'EOF'
Usage: register.sh --host 10.230.50.LAST --name oe-rva23-qemu-LAST [--allow-degraded]

Reads one short-lived repository Runner registration token from standard input,
or from OE_RUNNER_REGISTRATION_TOKEN in this process. The value is never an
argument, file, service environment, or log field.
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
oe_load_identity
[[ $OE_IDENTITY_HOST == "$OE_ARG_HOST" && $OE_IDENTITY_NAME == "$OE_ARG_NAME" ]] || oe_die 'installed identity does not match arguments'
[[ $OE_IDENTITY_ALLOW_DEGRADED == "$OE_ARG_ALLOW_DEGRADED" ]] \
  || oe_die 'registration --allow-degraded must exactly match the installed identity policy'
oe_load_policy
oe_check_no_other_runners "$OE_ARG_NAME"

runner_dir=$(oe_runner_dir "$OE_ARG_NAME")
service=$(oe_service_name "$OE_ARG_NAME")
[[ -x $runner_dir/config.sh && -x $runner_dir/bin/Runner.Listener ]] || oe_die 'install.sh must complete first'
[[ $(oe_runner_version "$runner_dir/bin/Runner.Listener" "$runner_dir") == 2.336.0 ]] \
  || oe_die 'Runner payload is not the pinned version'

if [[ -r $runner_dir/.runner ]]; then
  python3 - "$runner_dir/.runner" "$OE_ARG_NAME" "$oe_runner_repo_url" <<'PY'
import json
import pathlib
import sys

path, expected_name, expected_url = sys.argv[1:]
document = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
if document.get("agentName") != expected_name or document.get("gitHubUrl", "").rstrip("/") != expected_url:
    raise SystemExit("existing .runner identity does not match requested repository/name")
if document.get("workFolder") != "_work":
    raise SystemExit("existing .runner work folder is not _work")
PY
  oe_systemctl disable --now "$service" >/dev/null 2>&1 || true
  printf 'Runner %s is already registered with the expected identity and remains offline until activate.sh.\n' "$OE_ARG_NAME"
  exit 0
fi

oe_systemctl --quiet is-active "$service" && oe_die 'unconfigured Runner service is unexpectedly active'
oe_read_secret OE_RUNNER_REGISTRATION_TOKEN 'Short-lived Runner registration token: '
trap 'oe_wipe_secret; chown root:root "$runner_dir" 2>/dev/null || true' EXIT
chown "$oe_runner_user:$oe_runner_group" "$runner_dir"
printf '%s\n' "$OE_READ_SECRET" \
  | "$oe_runner_libexec/credential_exec.py" register --user "$oe_runner_user" --name "$OE_ARG_NAME"
oe_wipe_secret

[[ -r $runner_dir/.runner && -r $runner_dir/.credentials ]] || oe_die 'Runner configuration did not create required identity files'
chown root:root "$runner_dir"
for protected in .runner .credentials .credentials_rsaparams .service .env .path; do
  if [[ -e $runner_dir/$protected ]]; then
    [[ ! -L $runner_dir/$protected ]] || oe_die "Runner configuration file is a symlink: $protected"
    chown root:"$oe_runner_group" "$runner_dir/$protected"
    chmod 0640 "$runner_dir/$protected"
  fi
done
chown -R "$oe_runner_user:$oe_runner_group" "$runner_dir/_work" "$runner_dir/_diag" "$runner_dir/_state"
chmod 0700 "$runner_dir/_work" "$runner_dir/_diag" "$runner_dir/_state" \
  "$runner_dir/_state/home" "$runner_dir/_state/docker" "$runner_dir/_state/baseline"
trap - EXIT

oe_systemctl disable --now "$service" >/dev/null 2>&1 || true
printf 'Registered %s on %s; it remains offline until activate.sh passes the enabled policy.\n' "$OE_ARG_NAME" "$OE_ARG_HOST"
