#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libfreeaptx libfreeaptx-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
dd if=/dev/zero of="$smoke_dir/input.s24le" bs=24 count=10 status=none
freeaptxenc <"$smoke_dir/input.s24le" >"$smoke_dir/standard.aptx"
freeaptxdec <"$smoke_dir/standard.aptx" >"$smoke_dir/standard.s24le"
test -s "$smoke_dir/standard.aptx"
test "$(wc -c <"$smoke_dir/standard.s24le")" -eq 240
freeaptxenc --hd <"$smoke_dir/input.s24le" >"$smoke_dir/hd.aptx"
freeaptxdec --hd <"$smoke_dir/hd.aptx" >"$smoke_dir/hd.s24le"
test -s "$smoke_dir/hd.aptx"
test "$(wc -c <"$smoke_dir/hd.s24le")" -eq 240
cat >"$smoke_dir/version.c" <<'EOF'
#include <freeaptx.h>
int main(void) {
    return aptx_major == FREEAPTX_MAJOR && aptx_minor == FREEAPTX_MINOR &&
           aptx_patch == FREEAPTX_PATCH ? 0 : 1;
}
EOF
cc "$smoke_dir/version.c" $(pkg-config --cflags --libs libfreeaptx) -o "$smoke_dir/version"
"$smoke_dir/version"
