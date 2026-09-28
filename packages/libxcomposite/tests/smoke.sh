#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXcomposite
pkg-config --modversion xcomposite | grep -Fx '0.4.7'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/extensions/Xcomposite.h>

int main(void)
{
    return XCompositeVersion() == XCOMPOSITE_VERSION ? 0 : 1;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xcomposite) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xcomposite) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
