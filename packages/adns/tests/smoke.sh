#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

adnshost --version | grep -F '1.6.2'

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

cat >"$tmpdir/smoke.c" <<'EOF'
#include <adns.h>

int main(void) {
  adns_state state = 0;
  int result = adns_init_strcfg(
      &state, adns_if_noenv, 0, "nameserver 127.0.0.1");
  if (result != 0) {
    return result;
  }
  adns_finish(state);
  return 0;
}
EOF

${CC:-cc} ${CFLAGS:-} "$tmpdir/smoke.c" -ladns -o "$tmpdir/smoke"
"$tmpdir/smoke"
