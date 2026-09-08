#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lz4 lz4-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler RISC-V LZ4 smoke\n' >"$smoke_dir/input"
lz4 -q "$smoke_dir/input" "$smoke_dir/input.lz4"
lz4 -q -d "$smoke_dir/input.lz4" "$smoke_dir/output"
cmp "$smoke_dir/input" "$smoke_dir/output"
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <lz4.h>
#include <string.h>
int main(void) {
    const char input[] = "LZ4 library smoke";
    char output[128];
    int size = LZ4_compress_default(input, output, (int)strlen(input), sizeof(output));
    return size > 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" -llz4 -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
