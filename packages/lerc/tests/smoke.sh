#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <Lerc_c_api.h>
#include <math.h>
#include <stdlib.h>

int main(void) {
  float input[4] = {1.0f, 2.0f, 4.0f, 8.0f};
  float output[4] = {0};
  unsigned int needed = 0;
  unsigned int written = 0;
  if (lerc_computeCompressedSize(input, 6, 1, 2, 2, 1, 0, NULL, 0.0,
                                 &needed) != 0 || needed == 0) {
    return 1;
  }
  unsigned char *blob = malloc(needed);
  if (!blob) {
    return 2;
  }
  if (lerc_encode(input, 6, 1, 2, 2, 1, 0, NULL, 0.0, blob, needed,
                  &written) != 0 || written == 0 ||
      lerc_decode(blob, written, 0, NULL, 1, 2, 2, 1, 6, output) != 0) {
    free(blob);
    return 3;
  }
  free(blob);
  for (int i = 0; i < 4; ++i) {
    if (fabsf(input[i] - output[i]) > 0.00001f) {
      return 4;
    }
  }
  return 0;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" \
  $(pkg-config --cflags --libs Lerc) -lm -o "$tmpdir/smoke"
"$tmpdir/smoke"
