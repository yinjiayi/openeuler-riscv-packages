#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- zlib-ng zlib-ng-devel zlib-ng-static
test "$(pkg-config --modversion zlib-ng)" = "2.3.3"

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <zlib-ng.h>
#include <stdint.h>
#include <string.h>

int main(void) {
    static const uint8_t input[] = "openEuler riscv64 RVA23 zlib-ng smoke";
    uint8_t compressed[256];
    uint8_t restored[256];
    size_t compressed_len = sizeof(compressed);
    size_t restored_len = sizeof(restored);
    if (zng_compress2(compressed, &compressed_len, input, sizeof(input),
                      Z_BEST_COMPRESSION) != Z_OK)
        return 1;
    if (zng_uncompress(restored, &restored_len, compressed, compressed_len) != Z_OK)
        return 2;
    return restored_len != sizeof(input) || memcmp(restored, input, sizeof(input)) != 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs zlib-ng) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
