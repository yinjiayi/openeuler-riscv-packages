#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXt libXt-devel
pkg-config --modversion xt | grep -Fx '1.3.1'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Intrinsic.h>
#include <string.h>

int main(void)
{
    char *buffer = XtMalloc(8);
    if (buffer == NULL)
        return 1;
    strcpy(buffer, "libXt");
    int result = strcmp(buffer, "libXt") != 0;
    XtFree(buffer);
    return result;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xt) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xt) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
