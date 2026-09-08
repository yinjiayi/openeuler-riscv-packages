#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT

printf 'sp_arith = force\n' >"$tmpdir/uncrustify.cfg"
printf 'int main(){return 1+2;}\n' >"$tmpdir/input.c"
uncrustify -q -c "$tmpdir/uncrustify.cfg" -f "$tmpdir/input.c" -o "$tmpdir/output.c"
grep -F 'return 1 + 2;' "$tmpdir/output.c"
