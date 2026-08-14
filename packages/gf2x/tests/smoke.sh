#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <gf2x.h>

int main(void) {
  const unsigned long a[1] = {3UL};
  const unsigned long b[1] = {5UL};
  unsigned long product[2] = {0UL, 0UL};

  if (gf2x_mul(product, a, 1, b, 1) != 0) {
    return 1;
  }
  return product[0] == 15UL && product[1] == 0UL ? 0 : 2;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" \
  $(pkg-config --cflags --libs gf2x) -o "$tmpdir/smoke"
"$tmpdir/smoke"
