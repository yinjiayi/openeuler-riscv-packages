#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXss
pkg-config --modversion xscrnsaver | grep -Fx '1.2.5'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Xlib.h>
#include <X11/extensions/scrnsaver.h>

int main(void)
{
    XScreenSaverInfo *info = XScreenSaverAllocInfo();
    if (!info)
        return 1;
    info->window = None;
    return XFree(info) == 1 ? 0 : 2;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xscrnsaver x11) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xscrnsaver x11) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
