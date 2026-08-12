#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libbase58 libbase58-devel
rpm -q --provides libbase58 | grep -F 'libbase58.so.0()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
printf '\0RVA23' >"$smoke_dir/input.bin"
base58 <"$smoke_dir/input.bin" >"$smoke_dir/encoded.txt"
base58 -d 6 <"$smoke_dir/encoded.txt" >"$smoke_dir/decoded.bin"
cmp "$smoke_dir/input.bin" "$smoke_dir/decoded.bin"

cat >"$smoke_dir/libbase58-smoke.c" <<'EOF'
#include <libbase58.h>
#include <stdbool.h>
#include <stddef.h>

int main(void) {
    static const unsigned char input[] = {0, 'R', 'V', 'A', '2', '3'};
    char encoded[32];
    unsigned char decoded[sizeof input];
    size_t encoded_size = sizeof encoded;
    size_t decoded_size = sizeof decoded;
    if (!b58enc(encoded, &encoded_size, input, sizeof input))
        return 1;
    if (!b58tobin(decoded, &decoded_size, encoded, encoded_size - 1))
        return 1;
    if (decoded_size != sizeof input)
        return 1;
    for (size_t i = 0; i < sizeof input; ++i)
        if (decoded[i] != input[i])
            return 1;
    return 0;
}
EOF
cc "$smoke_dir/libbase58-smoke.c" -o "$smoke_dir/libbase58-smoke" \
  $({ pkg-config --cflags --libs libbase58; })
"$smoke_dir/libbase58-smoke"
