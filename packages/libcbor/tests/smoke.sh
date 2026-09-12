#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libcbor libcbor-devel
pkg-config --modversion libcbor | grep -Fx '0.14.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libcbor-smoke.c" <<'EOF'
#include <cbor.h>
#include <stdlib.h>

int main(void) {
    cbor_item_t *encoded = cbor_build_uint8(42);
    cbor_item_t *decoded;
    struct cbor_load_result result;
    unsigned char *buffer = NULL;
    size_t buffer_size = 0;
    size_t written;
    int ok;

    if (encoded == NULL)
        return 1;
    written = cbor_serialize_alloc(encoded, &buffer, &buffer_size);
    if (written == 0 || buffer == NULL)
        return 2;
    decoded = cbor_load(buffer, written, &result);
    ok = decoded != NULL && cbor_isa_uint(decoded) &&
         cbor_get_int(decoded) == 42;
    cbor_decref(&encoded);
    if (decoded != NULL)
        cbor_decref(&decoded);
    free(buffer);
    return ok ? 0 : 3;
}
EOF

read -r -a pkg_flags <<<"$(pkg-config --cflags --libs libcbor)"
cc "$smoke_dir/libcbor-smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/libcbor-smoke"
"$smoke_dir/libcbor-smoke"
