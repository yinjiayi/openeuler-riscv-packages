#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXrender
pkg-config --modversion xrender | grep -Fx '0.9.12'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <stddef.h>
#include <X11/extensions/Xrender.h>

int main(void)
{
    XRenderColor color = {0};
    char valid[] = "rgba:f/0/0/f";
    char invalid[] = "rgba:g/0/0/f";

    if (!XRenderParseColor(NULL, valid, &color))
        return 1;
    if (color.red != 0xffff || color.green != 0 ||
        color.blue != 0 || color.alpha != 0xffff)
        return 2;
    if (XRenderParseColor(NULL, invalid, &color))
        return 3;
    return 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xrender) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xrender) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
