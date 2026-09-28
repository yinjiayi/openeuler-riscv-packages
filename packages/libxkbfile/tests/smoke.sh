#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libxkbfile libxkbfile-devel
pkg-config --modversion xkbfile | grep -Fx '1.2.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Xlib.h>
#include <X11/extensions/XKBrules.h>

int main(void)
{
    XkbRF_RulesPtr rules = XkbRF_Create(2, 1);
    if (rules == NULL || rules->sz_rules != 2 || rules->sz_extra != 1)
        return 1;
    XkbRF_Free(rules, True);
    return 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  "$smoke_dir/smoke.c" \
  $(pkg-config --cflags --libs xkbfile) \
  -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
