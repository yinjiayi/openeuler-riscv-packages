#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libHX libHX-devel
pkg-config --modversion libHX | grep -Fx '5.4'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/libhx-smoke.c" <<'EOF'
#include <libHX/string.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char *copy = HX_strdup("RVA23");
    int result;

    if (copy == NULL)
        return 1;
    result = strcmp(copy, "RVA23");
    free(copy);
    return result == 0 ? 0 : 2;
}
EOF

cc $({ pkg-config --cflags libHX; }) "$smoke_dir/libhx-smoke.c" \
  -o "$smoke_dir/libhx-smoke" $({ pkg-config --libs libHX; })
"$smoke_dir/libhx-smoke"
