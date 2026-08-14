#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- patchelf
patchelf --version | grep -F 'patchelf 0.19.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/patchelf-smoke.c" <<'EOF'
#include <stdio.h>

int main(void) {
    puts("patchelf-rva23-ok");
    return 0;
}
EOF
cc "$smoke_dir/patchelf-smoke.c" -o "$smoke_dir/patchelf-smoke"
test -n "$(patchelf --print-interpreter "$smoke_dir/patchelf-smoke")"
patchelf --set-rpath '$ORIGIN' "$smoke_dir/patchelf-smoke"
test "$(patchelf --print-rpath "$smoke_dir/patchelf-smoke")" = '$ORIGIN'
test "$("$smoke_dir/patchelf-smoke")" = 'patchelf-rva23-ok'
