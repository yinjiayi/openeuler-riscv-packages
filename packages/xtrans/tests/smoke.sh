#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- xtrans
pkg-config --modversion xtrans | grep -Fx '1.6.0'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

# Consumers compile the installed transport source into their own binary.
${CC:-cc} -std=gnu99 -DICE_t -DTCPCONN -DUNIXCONN \
  $(pkg-config --cflags xtrans) \
  -c /usr/include/X11/Xtrans/transport.c -o "$smoke_dir/transport.o"

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/Xtrans/Xtrans.h>

int main(void)
{
    XtransConnInfo connection = 0;
    return connection != 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xtrans) \
  "$smoke_dir/smoke.c" -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
