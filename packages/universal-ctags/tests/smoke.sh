#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- universal-ctags
ctags --version | grep -F 'Universal Ctags 6.2.1'
tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/rva23.c" <<'EOF'
static int rva23_symbol(void) { return 23; }
EOF
ctags -f "$tmpdir/tags" "$tmpdir/rva23.c"
grep -q '^rva23_symbol' "$tmpdir/tags"
readtags -t "$tmpdir/tags" - rva23_symbol | grep -q 'rva23_symbol'
