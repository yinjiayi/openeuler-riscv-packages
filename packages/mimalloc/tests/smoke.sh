#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- mimalloc mimalloc-devel mimalloc-static
test -r /usr/include/mimalloc.h
test -r /usr/lib64/libmimalloc.so.3
test -r /usr/lib64/libmimalloc.a
test -r /usr/lib64/pkgconfig/mimalloc.pc
test "$(pkg-config --modversion mimalloc)" = "3.5"

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/mimalloc-smoke.c" <<'EOF'
#include <mimalloc.h>
#include <string.h>

int main(void) {
    static const char message[] = "openEuler riscv64 RVA23 mimalloc smoke";
    char *copy;

    if (MI_MALLOC_VERSION != 30502 || mi_version() != 30502)
        return 1;
    copy = mi_malloc(sizeof(message));
    if (copy == NULL)
        return 2;
    memcpy(copy, message, sizeof(message));
    if (memcmp(copy, message, sizeof(message)) != 0) {
        mi_free(copy);
        return 3;
    }
    mi_free(copy);
    return 0;
}
EOF
cc "$smoke_dir/mimalloc-smoke.c" \
  $({ pkg-config --cflags --libs mimalloc; }) \
  -o "$smoke_dir/mimalloc-smoke"
"$smoke_dir/mimalloc-smoke"
