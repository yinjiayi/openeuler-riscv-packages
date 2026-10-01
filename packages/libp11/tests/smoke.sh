#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libp11 libp11-devel
test "$(pkg-config --modversion libp11)" = 0.4.21

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'C'
#include <libp11.h>

int main(void) {
    PKCS11_CTX *ctx = PKCS11_CTX_new();
    if (ctx == NULL)
        return 1;
    PKCS11_CTX_free(ctx);
    return 0;
}
C

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libp11) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
