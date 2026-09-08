#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <lfp.h>
#include <unistd.h>

int main(void) {
  char path[] = "/tmp/libfixposix-smoke-XXXXXX";
  int fd = lfp_mkstemp(path);
  if (fd < 0) {
    return 1;
  }
  if (close(fd) != 0) {
    unlink(path);
    return 2;
  }
  return unlink(path) == 0 ? 0 : 3;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" \
  $(pkg-config --cflags --libs libfixposix) -o "$tmpdir/smoke"
"$tmpdir/smoke"
