#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- snappy snappy-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/smoke.c" <<'EOF'
#include <snappy-c.h>
#include <string.h>
int main(void) {
    const char input[] = "openEuler RISC-V Snappy smoke";
    char compressed[128];
    char output[128];
    size_t compressed_size = sizeof(compressed);
    size_t output_size = sizeof(output);
    if (snappy_compress(input, strlen(input), compressed, &compressed_size) != SNAPPY_OK) return 1;
    if (snappy_uncompress(compressed, compressed_size, output, &output_size) != SNAPPY_OK) return 2;
    return output_size == strlen(input) && memcmp(input, output, output_size) == 0 ? 0 : 3;
}
EOF
cc "$smoke_dir/smoke.c" -lsnappy -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
