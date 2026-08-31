#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- dosfstools
test -x /usr/sbin/mkfs.fat
test -x /usr/sbin/fsck.fat

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
image="$smoke_dir/fat.img"
dd if=/dev/zero of="$image" bs=1024 count=1440 >/dev/null 2>&1
mkfs_output="$smoke_dir/mkfs.out"
mkfs.fat -F 12 -n B6TEST "$image" >"$mkfs_output" 2>&1
grep -F 'mkfs.fat 4.2' "$mkfs_output"
test "$(fatlabel "$image")" = B6TEST
fsck_output="$smoke_dir/fsck.out"
fsck.fat -V -n "$image" >"$fsck_output" 2>&1
grep -F 'fsck.fat 4.2' "$fsck_output"
