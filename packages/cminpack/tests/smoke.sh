#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cminpack cminpack-devel
rpm -q --provides cminpack | grep -F 'libcminpack.so.1()(64bit)'
rpm -q --provides cminpack | grep -F 'libcminpacks.so.1()(64bit)'
rpm -q --provides cminpack | grep -F 'libcminpackld.so.1()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/cminpack-smoke.c" <<'EOF'
#include <cminpack.h>

int main(void) {
    double epsilon = dpmpar(1);
    return epsilon > 0.0 && epsilon < 1.0 ? 0 : 1;
}
EOF
cc $({ pkg-config --cflags cminpack; }) \
  "$smoke_dir/cminpack-smoke.c" -o "$smoke_dir/cminpack-smoke" \
  $({ pkg-config --libs cminpack; })
"$smoke_dir/cminpack-smoke"
