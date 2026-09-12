#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- clzip
clzip -V | grep -F 'clzip 1.16'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf 'openEuler RISC-V clzip smoke\n' >"$smoke_dir/input.txt"
clzip -qk "$smoke_dir/input.txt"
clzip -qcd "$smoke_dir/input.txt.lz" >"$smoke_dir/output.txt"
cmp "$smoke_dir/input.txt" "$smoke_dir/output.txt"
