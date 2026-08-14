#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <cglm/call.h>
#include <math.h>

int main(void) {
  mat4 identity;
  vec4 input = {1.0f, 2.0f, 3.0f, 1.0f};
  vec4 output;
  glm_mat4_identity(identity);
  glmc_mat4_mulv(identity, input, output);
  for (int i = 0; i < 4; ++i) {
    if (fabsf(input[i] - output[i]) > 0.00001f) {
      return 1;
    }
  }
  return 0;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" \
  $(pkg-config --cflags --libs cglm) -lm -o "$tmpdir/smoke"
"$tmpdir/smoke"
