#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuo pipefail
set +x

source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
# shellcheck source=_lib.sh
source "$source_dir/_lib.sh"

usage() {
  printf 'Usage: cleanup.sh --name oe-rva23-qemu-LAST --phase before|after\n'
}

name=
phase=
oe_reject_secret_arguments "$@"
while (($#)); do
  case $1 in
    --name) (($# >= 2)) || oe_usage_error '--name needs a value'; name=$2; shift 2 ;;
    --phase) (($# >= 2)) || oe_usage_error '--phase needs a value'; phase=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) oe_usage_error "unknown argument: $1" ;;
  esac
done
[[ -n $name && $phase =~ ^(before|after)$ ]] || oe_usage_error '--name and --phase before|after are required'
host=$(oe_host_from_name "$name")
oe_assert_local_host "$host"
oe_load_identity
[[ $OE_IDENTITY_HOST == "$host" && $OE_IDENTITY_NAME == "$name" ]] || oe_die 'installed identity does not match cleanup target'

runner_dir=$(oe_runner_dir "$name")
work_dir=$runner_dir/_work
state_dir=$runner_dir/_state
[[ -d $oe_runner_base && ! -L $oe_runner_base && $(stat -c '%U:%G:%a' "$oe_runner_base") == root:root:755 ]] \
  || oe_die 'managed Runner base directory is missing or unsafe'
[[ -d $runner_dir && ! -L $runner_dir && $(stat -c '%U:%G:%a' "$runner_dir") == root:root:755 ]] \
  || oe_die 'managed Runner directory is missing or unsafe'
[[ -d $work_dir && ! -L $work_dir && $work_dir == "$oe_runner_base/$name/_work" ]] || oe_die 'managed work directory is missing or unsafe'
[[ -d $state_dir && ! -L $state_dir && $state_dir == "$oe_runner_base/$name/_state" ]] || oe_die 'managed state directory is missing or unsafe'
for directory in "$work_dir" "$state_dir" "$state_dir/home" "$state_dir/docker"; do
  [[ -d $directory && ! -L $directory ]] || oe_die "managed cleanup directory is missing or unsafe: $directory"
done

cleanup_lock=$state_dir/cleanup.lock
exec 9>"$cleanup_lock"
flock --exclusive --timeout 60 9 || oe_die 'cleanup lock timed out'

# This is safe only because identity/fleet checks above prove that this is the
# one dedicated Runner host. Any running container is unexpected, so the
# helper aborts before mutation instead of guessing ownership.
"$oe_runner_libexec/docker-cleanup.py" --docker /usr/bin/docker --max-objects 512

# QEMU builds can leave root-owned files in bind mounts. Use only the already
# cached, repository digest-locked base image to remove verified directory
# children as container root. --pull=never prevents cleanup from adding a
# network fetch. Before the first image pull, these directories are user-owned
# and the host fallback is sufficient.
oe_load_cleanup_image_lock "$oe_runner_config/cleanup-image.lock"
if oe_run docker image inspect "$CLEANUP_IMAGE_REF" >/dev/null 2>&1; then
  oe_run docker run --rm --pull never --platform linux/riscv64 \
    --network none --read-only --memory 1g --cpus 1 --pids-limit 128 \
    --security-opt no-new-privileges --user 0:0 \
    --mount "type=bind,src=$work_dir,dst=/cleanup/work" \
    --mount "type=bind,src=$state_dir/home,dst=/cleanup/home" \
    --mount "type=bind,src=$state_dir/docker,dst=/cleanup/docker" \
    "$CLEANUP_IMAGE_REF" /bin/sh -euc \
    'find /cleanup/work /cleanup/home /cleanup/docker -mindepth 1 -maxdepth 1 -xdev -exec rm -rf -- {} +'
else
  find "$work_dir" "$state_dir/home" "$state_dir/docker" \
    -mindepth 1 -maxdepth 1 -xdev -exec rm -rf -- {} +
fi
install -d -o "$oe_runner_user" -g "$oe_runner_group" -m 0700 "$work_dir/_temp" "$work_dir/_tool"

printf 'Runner workspace cleanup completed (%s).\n' "$phase"
