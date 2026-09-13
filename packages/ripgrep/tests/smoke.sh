#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- ripgrep
test -x /usr/bin/rg
manpage=$(find /usr/share/man/man1 -maxdepth 1 -type f -name 'rg.1*' -print -quit)
test -n "$manpage"
test -s "$manpage"
test -s /usr/share/bash-completion/completions/rg

tmpdir=$(mktemp -d)
trap 'rm -rf -- "$tmpdir"' EXIT
printf 'ordinary line\nRVA23 package smoke\n' >"$tmpdir/input.txt"
rg -n -F 'RVA23 package smoke' "$tmpdir/input.txt" | grep -Fq '2:RVA23 package smoke'
if rg -q -F 'missing pattern' "$tmpdir/input.txt"; then
  exit 1
fi
