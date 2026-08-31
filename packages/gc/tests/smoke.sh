#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- gc gc-devel
libdir=$(rpm --eval '%{_libdir}')
rpm -qf -- "$libdir/libcord.so.1"
d=$(mktemp -d); trap 'rm -rf "$d"' EXIT
cat >"$d/smoke.c" <<'EOF'
#include <gc.h>
#include <string.h>
int main(void) {
    GC_INIT();
    char *p = GC_MALLOC_ATOMIC(32);
    if (!p) return 1;
    strcpy(p, "openEuler-RVA23");
    GC_gcollect();
    return strcmp(p, "openEuler-RVA23") == 0 ? 0 : 2;
}
EOF
gcc "$d/smoke.c" -o "$d/smoke" $(pkg-config --cflags --libs bdw-gc)
"$d/smoke"
