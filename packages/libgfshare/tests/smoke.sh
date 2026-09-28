#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libgfshare libgfshare-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

(
  cd "$smoke_dir"
  printf 'openEuler RISC-V secret sharing\n' > plain
  gfsplit -n 2 -m 3 plain share
  set -- share.*
  test "$#" -eq 3
  gfcombine "$1" "$2"
  cmp plain share
)

cat >"$smoke_dir/check.c" <<'EOF'
#include <libgfshare.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/random.h>
static void fill_random(unsigned char *buf, unsigned int count) {
    while (count) {
        ssize_t n = getrandom(buf, count, 0);
        if (n < 0 && errno == EINTR) continue;
        if (n <= 0) abort();
        buf += n;
        count -= n;
    }
}
int main(void) {
    unsigned char numbers[2] = {1, 2};
    gfshare_fill_rand = fill_random;
    gfshare_ctx *ctx = gfshare_ctx_init_dec(numbers, 2, 1);
    if (ctx == 0) return 1;
    gfshare_ctx_free(ctx);
    return 0;
}
EOF
cc "$smoke_dir/check.c" $(pkg-config --cflags --libs libgfshare) -o "$smoke_dir/check"
"$smoke_dir/check"
