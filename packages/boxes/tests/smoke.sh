#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- boxes
boxes --version | grep -F '2.3.2'
test -f /usr/share/boxes
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler RISC-V\n' > "$smoke_dir/plain"
boxes -d c < "$smoke_dir/plain" > "$smoke_dir/boxed"
grep -F 'openEuler RISC-V' "$smoke_dir/boxed"
boxes -d c -r < "$smoke_dir/boxed" > "$smoke_dir/roundtrip"
cmp "$smoke_dir/plain" "$smoke_dir/roundtrip"
