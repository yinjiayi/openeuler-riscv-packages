#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXi
pkg-config --modversion xi | grep -Fx '1.8.3'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/extensions/XInput.h>
#include <X11/extensions/XInput2.h>

int main(void)
{
    int (*volatile query)(Display *, int *, int *) = XIQueryVersion;
    return query == 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xi) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xi) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
