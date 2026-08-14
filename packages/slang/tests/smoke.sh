#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- slang slang-devel slang-help
rpm -q --provides slang | grep -F 'libslang.so.2()(64bit)'
slsh -n -e 'vmessage("openEuler RVA23");' | grep -F 'openEuler RVA23'

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT
cat >"$smoke_dir/slang-smoke.c" <<'EOF'
#include <slang.h>

int main(void) {
    int value = 0;
    if (SLang_init_slang() == -1)
        return 1;
    if (SLang_push_integer(23) == -1)
        return 2;
    if (SLang_pop_integer(&value) == -1)
        return 3;
    return value == 23 ? 0 : 4;
}
EOF
cc $({ pkg-config --cflags slang; }) \
  "$smoke_dir/slang-smoke.c" -o "$smoke_dir/slang-smoke" \
  $({ pkg-config --libs slang; })
"$smoke_dir/slang-smoke"
