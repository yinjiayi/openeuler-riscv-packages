#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lzop
lzop --version | grep -F 'lzop v1.04'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler RVA23 lzop smoke\n' >"$smoke_dir/input"
lzop --no-name --output "$smoke_dir/input.lzo" "$smoke_dir/input"
lzop --test "$smoke_dir/input.lzo"
lzop --decompress --output "$smoke_dir/output" "$smoke_dir/input.lzo"
cmp "$smoke_dir/input" "$smoke_dir/output"
