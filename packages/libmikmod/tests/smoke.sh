#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libmikmod libmikmod-devel

smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <mikmod.h>

int main(void) {
    if (MikMod_GetVersion() < ((3L << 16) | (3L << 8)))
        return 1;
    MikMod_RegisterAllLoaders();
    return MikMod_InfoLoader() == 0;
}
EOF

cc "$smoke_dir/smoke.c" -lmikmod -lpthread -lm -ldl -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
