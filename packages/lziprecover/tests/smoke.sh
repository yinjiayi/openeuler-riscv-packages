#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lziprecover
lziprecover --version | sed -n '1p' | grep -Fx 'lziprecover 1.26'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf '%b' \
  '\x4c\x5a\x49\x50\x01\x0c\x00\x29\x15\x84\x23\x4f\x67\x7a\x97\x69\xbf\xff\xfe\xe0\x78\x00\xbc\xb0\x2e\x57\x06\x00\x00\x00\x00\x00\x00\x00\x2a\x00\x00\x00\x00\x00\x00\x00' \
  >"$smoke_dir/input.lz"
lziprecover -t "$smoke_dir/input.lz"
lziprecover -cd "$smoke_dir/input.lz" | grep -Fx 'RVA23'
