#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdivsufsort libdivsufsort-devel
pkg-config --modversion libdivsufsort | grep -Fx '2.0.1'
pkg-config --modversion libdivsufsort64 | grep -Fx '2.0.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/libdivsufsort-smoke.c" <<'EOF'
#include <divsufsort.h>
#include <divsufsort64.h>

int main(void) {
    const sauchar_t text[] = "banana";
    const saidx_t expected32[] = {5, 3, 1, 0, 4, 2};
    const saidx64_t expected64[] = {5, 3, 1, 0, 4, 2};
    saidx_t suffix32[6];
    saidx64_t suffix64[6];
    int i;

    if (divsufsort(text, suffix32, 6) != 0 ||
        divsufsort64(text, suffix64, 6) != 0)
        return 1;
    for (i = 0; i < 6; ++i) {
        if (suffix32[i] != expected32[i] || suffix64[i] != expected64[i])
            return 2;
    }
    return 0;
}
EOF

read -r -a pkg_flags <<<"$(pkg-config --cflags --libs libdivsufsort libdivsufsort64)"
cc "$smoke_dir/libdivsufsort-smoke.c" "${pkg_flags[@]}" \
  -o "$smoke_dir/libdivsufsort-smoke"
"$smoke_dir/libdivsufsort-smoke"
