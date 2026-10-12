#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lzip
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

printf 'openEuler RISC-V lzip smoke\n' >"$smoke_dir/input.txt"
lzip -k "$smoke_dir/input.txt"
lzip -cd "$smoke_dir/input.txt.lz" >"$smoke_dir/output.txt"
cmp "$smoke_dir/input.txt" "$smoke_dir/output.txt"
