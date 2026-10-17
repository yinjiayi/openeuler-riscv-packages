#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/version.c" <<'EOF'
#include <stdio.h>
#include <zimg.h>
int main(void) { unsigned a, b, c; zimg_get_version_info(&a, &b, &c); printf("%u.%u.%u\n", a, b, c); }
EOF
cc "$tmpdir/version.c" $(pkg-config --cflags --libs zimg) -o "$tmpdir/version"
"$tmpdir/version" | grep -Fx '3.0.6'
