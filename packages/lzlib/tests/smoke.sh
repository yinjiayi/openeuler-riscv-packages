#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lzlib lzlib-devel
minilzip -V | grep -F "minilzip 1.16"

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
printf 'openEuler RISC-V lzlib smoke\n' >"$smoke_dir/input.txt"
minilzip -qk "$smoke_dir/input.txt"
minilzip -qcd "$smoke_dir/input.txt.lz" >"$smoke_dir/output.txt"
cmp "$smoke_dir/input.txt" "$smoke_dir/output.txt"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <stdint.h>
#include <string.h>
#include <lzlib.h>

int main(void) {
    LZ_Encoder *encoder;
    if (LZ_api_version() != 1016 || strcmp(LZ_version(), "1.16") != 0) return 1;
    encoder = LZ_compress_open(1 << 12, 5, 0);
    if (encoder == 0) return 1;
    return LZ_compress_close(encoder);
}
EOF
cc "$smoke_dir/smoke.c" -llz -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
