#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXdamage
pkg-config --modversion xdamage | grep -Fx '1.1.7'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/extensions/Xdamage.h>

int main(void)
{
    Bool (*volatile query)(Display *, int *, int *) = XDamageQueryExtension;
    return query == 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xdamage) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xdamage) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
