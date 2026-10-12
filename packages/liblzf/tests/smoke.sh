#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liblzf liblzf-devel liblzf-tools
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <lzf.h>
#include <stdio.h>
#include <string.h>

int main(void) {
    const char input[] = "liblzf installed API round trip round trip round trip";
    unsigned char compressed[sizeof(input) * 2];
    char output[sizeof(input)];
    unsigned int compressed_size = lzf_compress(input, sizeof(input), compressed, sizeof(compressed));
    unsigned int output_size;
    if (compressed_size == 0) return 1;
    output_size = lzf_decompress(compressed, compressed_size, output, sizeof(output));
    if (output_size != sizeof(input) || memcmp(input, output, sizeof(input)) != 0) return 2;
    puts("liblzf-api-round-trip-ok");
    return 0;
}
EOF

cc "$smoke_dir/smoke.c" -llzf -o "$smoke_dir/smoke"
"$smoke_dir/smoke" | grep -Fx 'liblzf-api-round-trip-ok'
printf 'lzf-cli-00000000000000000000000000000000\n' > "$smoke_dir/input"
lzf < "$smoke_dir/input" > "$smoke_dir/compressed"
lzf -d < "$smoke_dir/compressed" > "$smoke_dir/output"
cmp "$smoke_dir/input" "$smoke_dir/output"
