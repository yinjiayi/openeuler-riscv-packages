#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  printf 'Usage: audit.sh --host 10.230.50.LAST --name oe-rva23-qemu-LAST [--allow-degraded]\n'
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
[[ $OE_IDENTITY_ALLOW_DEGRADED == "$OE_ARG_ALLOW_DEGRADED" ]] \
  || oe_die 'audit --allow-degraded must exactly match the installed identity policy'
oe_load_policy
oe_load_release_lock "$oe_runner_config/runner-release.lock"
runner_dir=$(oe_runner_dir "$OE_ARG_NAME")
service=$(oe_service_name "$OE_ARG_NAME")

[[ $OE_IDENTITY_HOST == "$OE_ARG_HOST" && $OE_IDENTITY_NAME == "$OE_ARG_NAME" ]] || oe_die 'installed identity does not match arguments'
[[ -x $runner_dir/bin/Runner.Listener ]] || oe_die 'Runner.Listener is missing'
[[ $(oe_runner_version "$runner_dir/bin/Runner.Listener" "$runner_dir") == "$RUNNER_VERSION" ]] \
  || oe_die 'Runner version differs from lock'
grep -Fxq "sha256=$RUNNER_SHA256" "$runner_dir/.release" || oe_die 'installed release evidence differs from lock'
[[ ! -L $runner_dir && $(stat -c '%U:%G:%a' "$runner_dir") == root:root:755 ]] || oe_die 'runner root ownership/mode is unsafe'
[[ -d $oe_runner_lock_dir && ! -L $oe_runner_lock_dir \
  && $(stat -c '%U:%G:%a' "$oe_runner_lock_dir") == root:root:755 ]] \
  || oe_die 'cleanup lock directory ownership/mode is unsafe'
cleanup_lock=$oe_runner_lock_dir/$OE_ARG_NAME.lock
[[ -f $cleanup_lock && ! -L $cleanup_lock \
  && $(stat -c '%U:%G:%a' "$cleanup_lock") == root:"$oe_runner_group":660 ]] \
  || oe_die 'cleanup lock ownership/mode is unsafe'
for directory in "$runner_dir/_work" "$runner_dir/_diag" "$runner_dir/_state"; do
  [[ ! -L $directory && $(stat -c '%U:%G:%a' "$directory") == "$oe_runner_user:$oe_runner_group:700" ]] \
    || oe_die "runner-writable directory ownership/mode is unsafe: $directory"
done
command -v docker >/dev/null || oe_die 'Docker client is missing'
docker info >/dev/null 2>&1 || oe_die 'Docker is unavailable'
oe_load_cleanup_image_lock "$oe_runner_config/cleanup-image.lock"
docker image inspect "$CLEANUP_IMAGE_REF" >/dev/null 2>&1 \
  || oe_die 'digest-locked cleanup image is not cached'
command -v qemu-riscv64 >/dev/null || oe_die 'qemu-riscv64 is missing'
[[ -r /proc/sys/fs/binfmt_misc/qemu-riscv64 ]] || oe_die 'qemu-riscv64 binfmt is missing'

registered=false
[[ -r $runner_dir/.runner && -r $runner_dir/.credentials ]] && registered=true
active=false
oe_systemctl --quiet is-active "$service" && active=true
enabled=false
oe_systemctl --quiet is-enabled "$service" && enabled=true

if [[ $OE_POLICY_ENROLLMENT_ENABLED == false && ( $active == true || $enabled == true ) ]]; then
  oe_die 'Runner is active/enabled while policy disables enrollment'
fi
if [[ $active == true ]]; then
  [[ $registered == true && $OE_POLICY_ENROLLMENT_ENABLED == true ]] || oe_die 'active Runner lacks registration or enabled policy'
  "$oe_runner_libexec/preflight.sh" --name "$OE_ARG_NAME" >&2
fi

printf '{"schema_version":1,"host":"%s","name":"%s","stage":"%s","runner_version":"%s","registered":%s,"policy_enabled":%s,"service_enabled":%s,"service_active":%s,"docker":true,"qemu_riscv64":true,"binfmt_riscv64":true}\n' \
  "$OE_ARG_HOST" "$OE_ARG_NAME" "$stage" "$RUNNER_VERSION" "$registered" "$OE_POLICY_ENROLLMENT_ENABLED" "$enabled" "$active"
