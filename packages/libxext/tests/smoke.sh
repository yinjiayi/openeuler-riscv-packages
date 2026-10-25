#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXext
pkg-config --modversion xext | grep -Fx '1.3.7'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Xlib.h>
#include <X11/Xproto.h>
#include <X11/extensions/extutil.h>

int main(void)
{
    XExtensionInfo *info = XextCreateExtension();
    if (info == NULL)
        return 1;
    if (info->head != NULL || info->cur != NULL || info->ndisplays != 0)
        return 2;
    XextDestroyExtension(info);
    return 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xext) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xext) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
