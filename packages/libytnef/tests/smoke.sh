#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libytnef libytnef-tools
pkg-config --print-errors --modversion libytnef | grep -Fx '2.1.2'
ytnef -h >/dev/null
command -v ytnefprint >/dev/null
command -v ytnefprocess >/dev/null

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <ytnef.h>

int main(void)
{
    TNEFStruct stream;
    TNEFInitialize(&stream);
    TNEFFree(&stream);
    return 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags libytnef) \
  "$smoke_dir/smoke.c" $(pkg-config --libs libytnef) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
