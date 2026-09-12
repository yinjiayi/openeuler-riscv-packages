#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmpack libmpack-devel
rpm -q --provides libmpack | grep -F 'libmpack.so.0()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libmpack-smoke.c" <<'EOF'
#include <mpack.h>

int main(void) {
    char encoded[16];
    char *output = encoded;
    size_t output_size = sizeof encoded;
    const char *input;
    size_t input_size;
    mpack_tokbuf_t writer;
    mpack_tokbuf_t reader;
    mpack_token_t token = mpack_pack_uint(23);
    mpack_token_t decoded;

    mpack_tokbuf_init(&writer);
    if (mpack_write(&writer, &output, &output_size, &token) != MPACK_OK)
        return 1;
    input = encoded;
    input_size = sizeof encoded - output_size;
    mpack_tokbuf_init(&reader);
    if (mpack_read(&reader, &input, &input_size, &decoded) != MPACK_OK)
        return 1;
    return decoded.type != MPACK_TOKEN_UINT || decoded.data.value.lo != 23;
}
EOF
cc "$smoke_dir/libmpack-smoke.c" -o "$smoke_dir/libmpack-smoke" \
  $({ pkg-config --cflags --libs mpack; })
"$smoke_dir/libmpack-smoke"
