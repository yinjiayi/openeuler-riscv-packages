#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libXtst
pkg-config --print-errors --modversion xtst | grep -Fx '1.2.5'

smoke_dir=$(mktemp -d)
trap 'rm -rf -- "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <X11/extensions/XTest.h>
#include <X11/extensions/record.h>

int main(void)
{
    Bool (*volatile test_query)(Display *, int *, int *, int *, int *) = XTestQueryExtension;
    Status (*volatile record_query)(Display *, int *, int *) = XRecordQueryVersion;
    return test_query == 0 || record_query == 0;
}
EOF

${CC:-cc} -std=c99 -Wall -Wextra -Werror \
  $(pkg-config --cflags xtst) \
  "$smoke_dir/smoke.c" $(pkg-config --libs xtst) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
