#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- zstd zstd-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf 'openEuler RISC-V Zstandard smoke\n' >"$smoke_dir/input"
zstd -q "$smoke_dir/input" -o "$smoke_dir/input.zst"
zstd -q -d "$smoke_dir/input.zst" -o "$smoke_dir/output"
cmp "$smoke_dir/input" "$smoke_dir/output"
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <zstd.h>
int main(void) {
    return ZSTD_compressBound(1024) > 1024 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" -lzstd -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
