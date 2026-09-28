#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libxls libxls-devel
pkg-config --modversion libxls | grep -Fx '1.6.3'
command -v xls2csv >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <xls.h>
#include <string.h>

int main(void) {
    return strcmp(xls_getVersion(), "1.6.3") == 0 ? 0 : 1;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs libxls) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"

if xls2csv "$smoke_dir/nonexistent.xls" >"$smoke_dir/invalid.out" 2>&1; then
  printf '%s\n' 'xls2csv unexpectedly accepted a missing workbook' >&2
  exit 1
fi
