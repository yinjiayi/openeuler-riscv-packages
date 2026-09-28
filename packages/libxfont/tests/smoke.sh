#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXfont2
pkg-config --print-errors --modversion xfont2 | grep -Fx '2.0.9'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <string.h>
#include <X11/Xfuncproto.h>
#include <X11/fonts/font.h>
#include <X11/fonts/fontstruct.h>
#include <X11/fonts/fontmisc.h>
#include <X11/fonts/libxfont2.h>

int main(void)
{
    FontNamesPtr names = xfont2_make_font_names_record(0);
    if (!names)
        return 1;
    if (xfont2_add_font_names_name(names, "fixed", 5) != Successful ||
        names->nnames != 1 || strcmp(names->names[0], "fixed") != 0) {
        xfont2_free_font_names(names);
        return 2;
    }
    xfont2_free_font_names(names);
    return 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xfont2) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xfont2) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
