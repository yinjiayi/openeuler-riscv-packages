#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libkate libkate-devel
smoke_dir=$(mktemp -d)
trap 'rm -rf "$smoke_dir"' EXIT

cat >"$smoke_dir/smoke.c" <<'EOF'
#include <kate/kate.h>
#include <kate/oggkate.h>
#include <string.h>

int main(void) {
    kate_info info;
    int ok = 1;
    if (kate_info_init(&info) < 0) return 1;
    if (kate_get_version() <= 0) ok = 0;
    if (!strstr(kate_get_version_string(), "0.4.3")) ok = 0;
    if (kate_ogg_decode_is_idheader(0) != 0) ok = 0;
    if (kate_info_clear(&info) < 0) ok = 0;
    return ok ? 0 : 2;
}
EOF

cc "$smoke_dir/smoke.c" $(pkg-config --cflags --libs oggkate) -o "$smoke_dir/smoke"
"$smoke_dir/smoke"
kateenc --version | grep -F '0.4.3'
