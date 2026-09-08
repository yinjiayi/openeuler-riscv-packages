#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libqb libqb-devel libqb-help doxygen2man
pkg-config --modversion libqb | grep -Fx '2.0.10'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT
cat >"$smoke_dir/libqb-smoke.c" <<'EOF'
#include <stddef.h>
#include <qb/qbarray.h>
#include <qb/qbutil.h>

int main(void) {
    qb_array_t *array;
    void *element = 0;

    if (qb_ver.major != 2 || qb_ver.minor != 0 || qb_ver.micro != 10)
        return 1;
    array = qb_array_create(4, sizeof(int));
    if (array == 0)
        return 2;
    if (qb_array_index(array, 2, &element) != 0 || element == 0)
        return 3;
    *(int *)element = 29;
    if (*(int *)element != 29)
        return 4;
    qb_array_free(array);
    return 0;
}
EOF
cc "$smoke_dir/libqb-smoke.c" -o "$smoke_dir/libqb-smoke" \
  $({ pkg-config --cflags --libs libqb; })
"$smoke_dir/libqb-smoke"
