#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libaec libaec-devel libaec-help

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libaec-smoke.c" <<'EOF'
#include <libaec.h>
#include <stdint.h>
#include <string.h>

int main(void) {
    const uint16_t input[16] = {
        1, 1, 2, 3, 5, 8, 13, 21,
        34, 55, 89, 144, 233, 377, 610, 987
    };
    uint16_t output[16] = {0};
    unsigned char compressed[512] = {0};
    struct aec_stream encoder = {0};
    struct aec_stream decoder = {0};
    size_t compressed_size;

    if (strcmp(AEC_VERSION_STRING, "1.1.7") != 0) {
        return 1;
    }
    encoder.next_in = (const unsigned char *)input;
    encoder.avail_in = sizeof(input);
    encoder.next_out = compressed;
    encoder.avail_out = sizeof(compressed);
    encoder.bits_per_sample = 16;
    encoder.block_size = 8;
    encoder.rsi = 2;
    encoder.flags = AEC_DATA_PREPROCESS;
    if (aec_buffer_encode(&encoder) != AEC_OK) {
        return 2;
    }
    compressed_size = encoder.total_out;

    decoder.next_in = compressed;
    decoder.avail_in = compressed_size;
    decoder.next_out = (unsigned char *)output;
    decoder.avail_out = sizeof(output);
    decoder.bits_per_sample = 16;
    decoder.block_size = 8;
    decoder.rsi = 2;
    decoder.flags = AEC_DATA_PREPROCESS;
    if (aec_buffer_decode(&decoder) != AEC_OK) {
        return 3;
    }
    return memcmp(input, output, sizeof(input)) == 0 ? 0 : 4;
}
EOF
cc "$smoke_dir/libaec-smoke.c" -o "$smoke_dir/libaec-smoke" -laec
"$smoke_dir/libaec-smoke"
