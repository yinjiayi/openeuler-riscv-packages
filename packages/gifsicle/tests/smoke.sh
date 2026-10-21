#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

# A complete one-pixel GIF89a image with a two-entry global color table.
printf 'GIF89a\001\000\001\000\200\000\000\000\000\000\377\377\377\041\371\004\001\000\000\000\000\054\000\000\000\000\001\000\001\000\000\002\002\104\001\000\073' > "$workdir/input.gif"

gifsicle --info "$workdir/input.gif" > "$workdir/info.txt"
grep -F '1 image' "$workdir/info.txt"
gifsicle --optimize=2 "$workdir/input.gif" > "$workdir/optimized.gif"
gifdiff "$workdir/input.gif" "$workdir/optimized.gif"

test "$(gifsicle --version | head -n 1)" = "LCDF Gifsicle 1.96"
test "$(gifdiff --version | head -n 1)" = "gifdiff (LCDF Gifsicle) 1.96"
test "$(gifview --version | head -n 1)" = "gifview (LCDF Gifsicle) 1.96"
