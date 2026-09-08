#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- xz xz-libs xz-devel xz-lzma-compat xz-help
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

printf 'openEuler riscv64 RVA23 XZ round-trip\n' >"$smoke_dir/input.txt"
xz --check=crc64 --threads=1 -c "$smoke_dir/input.txt" >"$smoke_dir/input.txt.xz"
xz -dc "$smoke_dir/input.txt.xz" >"$smoke_dir/output.txt"
cmp "$smoke_dir/input.txt" "$smoke_dir/output.txt"

lzma -c "$smoke_dir/input.txt" >"$smoke_dir/input.txt.lzma"
unlzma -c "$smoke_dir/input.txt.lzma" >"$smoke_dir/output-lzma.txt"
cmp "$smoke_dir/input.txt" "$smoke_dir/output-lzma.txt"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <lzma.h>
#include <stdint.h>
#include <string.h>

int main(void) {
    static const uint8_t input[] = "liblzma-riscv64-smoke";
    uint8_t encoded[256];
    uint8_t decoded[256];
    size_t encoded_pos = 0;
    size_t input_pos = 0;
    size_t decoded_pos = 0;
    uint64_t memory_limit = UINT64_MAX;

    if (lzma_easy_buffer_encode(6, LZMA_CHECK_CRC64, NULL, input,
                                sizeof(input), encoded, &encoded_pos,
                                sizeof(encoded)) != LZMA_OK)
        return 1;
    if (lzma_stream_buffer_decode(&memory_limit, 0, NULL, encoded, &input_pos,
                                  encoded_pos, decoded, &decoded_pos,
                                  sizeof(decoded)) != LZMA_OK)
        return 2;
    return decoded_pos != sizeof(input) || memcmp(input, decoded, sizeof(input));
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs liblzma) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
