#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- lzo lzo-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <lzo/lzo1x.h>
#include <string.h>
int main(void) {
    const unsigned char input[] = "openEuler-riscv64-RVA23";
    unsigned char compressed[128];
    unsigned char restored[128];
    unsigned char work[LZO1X_1_MEM_COMPRESS];
    lzo_uint compressed_len = sizeof(compressed);
    lzo_uint restored_len = sizeof(restored);
    if (lzo_init() != LZO_E_OK) return 1;
    if (lzo1x_1_compress(input, sizeof(input), compressed, &compressed_len, work) != LZO_E_OK) return 1;
    if (lzo1x_decompress_safe(compressed, compressed_len, restored, &restored_len, 0) != LZO_E_OK) return 1;
    return restored_len == sizeof(input) && memcmp(input, restored, sizeof(input)) == 0 ? 0 : 1;
}
EOF
cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs lzo2) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
