#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXxf86dga
pkg-config --modversion xxf86dga | grep -Fx '1.1.7'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Xlib.h>
#include <X11/extensions/Xxf86dga.h>
#include <X11/extensions/xf86dga1.h>

int main(void)
{
    Bool (*volatile query2)(Display *, int *, int *) = XDGAQueryVersion;
    Bool (*volatile query1)(Display *, int *, int *) = XF86DGAQueryVersion;
    return query1 == 0 || query2 == 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xxf86dga) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xxf86dga) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
