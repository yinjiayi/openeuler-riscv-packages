#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- liboggz liboggz-tools liboggz-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <oggz/oggz.h>

int main(void) {
    OGGZ *oggz = oggz_new(OGGZ_WRITE);
    if (!oggz) return 1;
    return oggz_close(oggz) == 0 ? 0 : 2;
}
EOF

${CC:-cc} ${CFLAGS:-} "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs oggz) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
