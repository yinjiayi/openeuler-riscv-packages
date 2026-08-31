#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  printf 'Usage: preflight.sh --name oe-rva23-qemu-LAST\n'
}

name=
oe_reject_secret_arguments "$@"
while (($#)); do
  case $1 in
    --name) (($# >= 2)) || oe_usage_error '--name needs a value'; name=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) oe_usage_error "unknown argument: $1" ;;
  esac
done
[[ -n $name ]] || oe_usage_error '--name is required'
host=$(oe_host_from_name "$name")
oe_assert_local_host "$host"
oe_load_identity
[[ $OE_IDENTITY_HOST == "$host" && $OE_IDENTITY_NAME == "$name" ]] || oe_die 'installed identity does not match service instance'
oe_assert_platform "$OE_IDENTITY_ALLOW_DEGRADED"
oe_load_policy
[[ $OE_POLICY_ENROLLMENT_ENABLED == true ]] || oe_die 'fleet enrollment is disabled by the root-owned policy'

runner_dir=$(oe_runner_dir "$name")
[[ -x $runner_dir/bin/Runner.Listener && -r $runner_dir/.runner ]] || oe_die 'runner is not configured'
[[ $(oe_runner_version "$runner_dir/bin/Runner.Listener" "$runner_dir") == 2.336.0 ]] \
  || oe_die 'runner version is not the pinned release'
[[ -S /run/docker.sock ]] || oe_die 'Docker socket is unavailable'
oe_run docker info >/dev/null 2>&1 || oe_die 'runner service account cannot reach Docker'
[[ -x /usr/sbin/iptables ]] \
  || oe_die 'Docker firewall helper is missing: /usr/sbin/iptables'
command -v qemu-riscv64 >/dev/null || oe_die 'qemu-riscv64 is missing'
[[ -r /proc/sys/fs/binfmt_misc/qemu-riscv64 ]] || oe_die 'qemu-riscv64 binfmt registration is missing'
grep -Fxq enabled /proc/sys/fs/binfmt_misc/qemu-riscv64 || oe_die 'qemu-riscv64 binfmt registration is disabled'

# GitHub downloads pinned action sources before any workflow step or job hook.
# Exercise the same GNU tar extraction path inside the systemd service sandbox
# so an incompatible syscall restriction fails before the Runner goes online.
tar_probe_dir=$(mktemp -d "$runner_dir/_state/.tar-extract-preflight.XXXXXX")
cleanup_tar_probe() {
  [[ -z ${tar_probe_dir:-} ]] || rm -rf -- "$tar_probe_dir"
}
trap cleanup_tar_probe EXIT
mkdir "$tar_probe_dir/source"
cp -- "$oe_runner_libexec/preflight.sh" "$tar_probe_dir/source/preflight.sh"
chmod 0755 "$tar_probe_dir/source/preflight.sh"
tar -czf "$tar_probe_dir/preflight.tar.gz" -C "$tar_probe_dir" source
mkdir "$tar_probe_dir/extracted"
tar -xzf "$tar_probe_dir/preflight.tar.gz" -C "$tar_probe_dir/extracted"
cmp -s "$oe_runner_libexec/preflight.sh" "$tar_probe_dir/extracted/source/preflight.sh" \
  || oe_die 'Runner service sandbox cannot faithfully extract a tar archive'
[[ -x $tar_probe_dir/extracted/source/preflight.sh ]] \
  || oe_die 'Runner service sandbox did not preserve the archive executable bit'
cleanup_tar_probe
tar_probe_dir=
trap - EXIT

printf 'Runner preflight passed for %s (%s).\n' "$name" "$host"
