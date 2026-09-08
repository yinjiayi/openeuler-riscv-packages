#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <uev/uev.h>

int main(void) {
  uev_ctx_t ctx;

  if (uev_init(&ctx) != 0)
    return 1;
  if (uev_run(&ctx, UEV_NONBLOCK) != 0)
    return 2;
  return uev_exit(&ctx) == 0 ? 0 : 3;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" $(pkg-config --cflags --libs libuev) -o "$tmpdir/smoke"
"$tmpdir/smoke"
