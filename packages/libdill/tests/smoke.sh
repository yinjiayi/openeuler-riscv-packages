#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libdill libdill-devel
pkg-config --exists libdill
rpm -q --qf '%{VERSION}\n' libdill | grep -Fx '2.14'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/libdill-smoke.c" <<'EOF'
#include <libdill.h>

static int worker_ran;

coroutine void worker(void) {
    worker_ran = 1;
}

int main(void) {
    int cr = go(worker());
    if (cr < 0)
        return 1;
    if (hclose(cr) < 0)
        return 2;
    return worker_ran ? 0 : 3;
}
EOF
read -r -a pkg_cflags <<<"$(pkg-config --cflags libdill)"
read -r -a pkg_libs <<<"$(pkg-config --libs libdill)"
cc -fno-stack-protector -fno-stack-clash-protection \
  "${pkg_cflags[@]}" "$smoke_dir/libdill-smoke.c" \
  -o "$smoke_dir/libdill-smoke" "${pkg_libs[@]}"
"$smoke_dir/libdill-smoke"
