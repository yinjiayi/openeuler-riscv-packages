#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- zopfli
zopfli -h >/dev/null 2>&1
zopflipng --help >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf 'openEuler RISC-V zopfli smoke\n' >"$smoke_dir/input.txt"
zopfli --i1 --gzip "$smoke_dir/input.txt"
test -s "$smoke_dir/input.txt.gz"
test "$(od -An -tx1 -N2 "$smoke_dir/input.txt.gz" | tr -d ' \n')" = "1f8b"
