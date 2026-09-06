#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

command -v qbe >/dev/null
tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT
cat >"$tmpdir/add.ssa" <<'EOF'
export function w $add(w %a, w %b) {
@start
  %r =w add %a, %b
  ret %r
}
EOF
qbe -t rv64 -o "$tmpdir/add.s" "$tmpdir/add.ssa"
grep -F '.text' "$tmpdir/add.s"
grep -F 'add' "$tmpdir/add.s"
