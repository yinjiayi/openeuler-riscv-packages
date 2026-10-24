#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXfixes
pkg-config --modversion xfixes | grep -Fx '6.0.2'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/extensions/Xfixes.h>

int main(void)
{
    return XFixesVersion() == XFIXES_VERSION ? 0 : 1;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xfixes) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xfixes) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
