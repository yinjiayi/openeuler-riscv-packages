#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libasyncns libasyncns-devel
pkg-config --modversion libasyncns | grep -Fx '0.8'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libasyncns-smoke.c" <<'EOF'
#include <asyncns.h>
#include <stddef.h>

int main(void) {
    asyncns_t *session = asyncns_new(1);
    int descriptor;

    if (session == NULL)
        return 1;
    descriptor = asyncns_fd(session);
    if (descriptor < 0 || asyncns_getnqueries(session) != 0) {
        asyncns_free(session);
        return 2;
    }
    asyncns_free(session);
    return 0;
}
EOF

read -r -a extra_cflags <<<"${CFLAGS:-}"
read -r -a pkg_flags <<<"$(pkg-config --cflags --libs libasyncns)"
"${CC:-cc}" "${extra_cflags[@]}" -pthread "$smoke_dir/libasyncns-smoke.c" \
  "${pkg_flags[@]}" -o "$smoke_dir/libasyncns-smoke"
"$smoke_dir/libasyncns-smoke"
