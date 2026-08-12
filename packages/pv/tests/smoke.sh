#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- pv

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf 'pv installed transfer smoke\nsecond line\n' >"$smoke_dir/input"
pv -q "$smoke_dir/input" >"$smoke_dir/output"
cmp "$smoke_dir/input" "$smoke_dir/output"
input_size=$(wc -c <"$smoke_dir/input")
pv -n -f -i 0.01 -s "$input_size" "$smoke_dir/input" \
  >/dev/null 2>"$smoke_dir/numeric"
tail -n 1 "$smoke_dir/numeric" | grep -Fx '100'
