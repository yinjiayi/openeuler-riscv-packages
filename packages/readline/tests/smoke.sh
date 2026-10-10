#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/version.c" <<'EOF'
#include <stdio.h>
#include <readline/readline.h>
int main(void) { puts(rl_library_version); return 0; }
EOF
cc "$tmpdir/version.c" $(pkg-config --cflags --libs readline) -o "$tmpdir/version"
"$tmpdir/version" | grep -Fx '8.3'
