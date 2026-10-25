#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libuecc libuecc-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/check.c" <<'EOF'
#include <libuecc/ecc.h>
#include <string.h>
int main(void) {
    ecc_int256_t packed, one = {{1}};
    ecc_25519_work_t point, loaded;
    ecc_25519_scalarmult_base(&point, &one);
    ecc_25519_store_packed_ed25519(&packed, &point);
    if (packed.p[0] != 0x58) return 1;
    for (unsigned i = 1; i < sizeof(packed.p); ++i)
        if (packed.p[i] != 0x66) return 2;
    if (!ecc_25519_load_packed_ed25519(&loaded, &packed)) return 3;
    ecc_25519_store_packed_ed25519(&one, &loaded);
    return memcmp(one.p, packed.p, sizeof(packed.p)) == 0 ? 0 : 4;
}
EOF
cc "$smoke_dir/check.c" $(pkg-config --cflags --libs libuecc) -o "$smoke_dir/check"
"$smoke_dir/check"
