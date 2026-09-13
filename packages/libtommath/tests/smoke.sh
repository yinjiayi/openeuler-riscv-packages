#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libtommath libtommath-devel libtommath-help
pkg-config --modversion libtommath | grep -Fx '1.3.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libtommath-smoke.c" <<'EOF'
#include <tommath.h>

int main(void) {
    mp_int a, b, product;
    if (mp_init_multi(&a, &b, &product, NULL) != MP_OKAY) {
        return 1;
    }
    mp_set_u32(&a, 23);
    mp_set_u32(&b, 44);
    if (mp_mul(&a, &b, &product) != MP_OKAY || mp_get_u32(&product) != 1012) {
        mp_clear_multi(&a, &b, &product, NULL);
        return 2;
    }
    mp_clear_multi(&a, &b, &product, NULL);
    return 0;
}
EOF
cc $({ pkg-config --cflags libtommath; }) "$smoke_dir/libtommath-smoke.c" \
  -o "$smoke_dir/libtommath-smoke" $({ pkg-config --libs libtommath; })
"$smoke_dir/libtommath-smoke"
