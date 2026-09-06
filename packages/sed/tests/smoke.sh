#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- sed
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

printf 'alpha=17\nbeta=23\n' >"$smoke_dir/input.txt"
sed -E 's/^([[:alpha:]]+)=([[:digit:]]+)$/\2:\1/' \
  "$smoke_dir/input.txt" >"$smoke_dir/output.txt"
printf '17:alpha\n23:beta\n' >"$smoke_dir/expected.txt"
cmp "$smoke_dir/expected.txt" "$smoke_dir/output.txt"

cp "$smoke_dir/input.txt" "$smoke_dir/in-place.txt"
sed -i 's/beta/RVA23/' "$smoke_dir/in-place.txt"
grep -Fx 'RVA23=23' "$smoke_dir/in-place.txt"
