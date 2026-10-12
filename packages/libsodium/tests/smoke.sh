#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libsodium libsodium-devel
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <sodium.h>
#include <string.h>
int main(void) {
    unsigned char digest[crypto_generichash_BYTES];
    const unsigned char msg[] = "RVA23";
    if (sodium_init() < 0) return 1;
    if (crypto_generichash(digest, sizeof digest, msg, strlen((const char *)msg), NULL, 0) != 0) return 2;
    return sodium_is_zero(digest, sizeof digest) ? 3 : 0;
}
EOF
gcc "$d/smoke.c" -o "$d/smoke" $(pkg-config --cflags --libs libsodium)
"$d/smoke"
