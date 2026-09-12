#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- rhash rhash-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

test "$(rhash --sha256 --one-hash -m abc)" = \
  "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <rhash.h>
#include <string.h>

int main(void) {
    static const char input[] = "abc";
    static const char expected[] =
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad";
    unsigned char digest[64];
    char output[129];
    rhash_library_init();
    if (rhash_msg(RHASH_SHA256, input, 3, digest) != 0)
        return 1;
    rhash_print_bytes(output, digest, rhash_get_digest_size(RHASH_SHA256), RHPR_HEX);
    return strcmp(output, expected) != 0;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs librhash) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
