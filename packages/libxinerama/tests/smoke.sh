#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXinerama
pkg-config --modversion xinerama | grep -Fx '1.1.6'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/extensions/Xinerama.h>
#include <X11/extensions/panoramiXext.h>

int main(void)
{
    Bool (*volatile query)(Display *, int *, int *) = XineramaQueryExtension;
    XineramaScreenInfo *(*volatile screens)(Display *, int *) = XineramaQueryScreens;
    return query == 0 || screens == 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xinerama) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xinerama) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
