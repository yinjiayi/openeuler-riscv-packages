#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- qhull qhull-devel qhull-help
rpm -q --provides qhull | grep -F 'libqhull.so.8.0()(64bit)'
rpm -q --provides qhull | grep -F 'libqhull_p.so.8.0()(64bit)'
rpm -q --provides qhull | grep -F 'libqhull_r.so.8.0()(64bit)'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
rbox 10 D2 | qhull s >"$smoke_dir/qhull.out" 2>&1
grep -F 'Number of vertices' "$smoke_dir/qhull.out"

cat >"$smoke_dir/qhull-smoke.c" <<'EOF'
#include <stdio.h>
#include <libqhull_r/qhull_ra.h>

int main(void) {
    coordT points[] = {0, 0, 1, 0, 0, 1, 1, 1};
    qhT qh_qh;
    qhT *qh = &qh_qh;
    qh_zero(qh, stderr);
    int rc = qh_new_qhull(qh, 2, 4, points, 0, "qhull Qt", NULL, stderr);
    qh_freeqhull(qh, !qh_ALL);
    int curlong = 0;
    int totlong = 0;
    qh_memfreeshort(qh, &curlong, &totlong);
    return rc == 0 && curlong == 0 && totlong == 0 ? 0 : 1;
}
EOF
cc $({ pkg-config --cflags qhull_r; }) \
  "$smoke_dir/qhull-smoke.c" -o "$smoke_dir/qhull-smoke" \
  $({ pkg-config --libs qhull_r; })
"$smoke_dir/qhull-smoke"
