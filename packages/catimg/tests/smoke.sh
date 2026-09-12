#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- catimg
catimg -h | grep -F 'Usage: catimg'
test -r /usr/share/man/man1/catimg.1.gz
test -r /usr/share/zsh/site-functions/_catimg
sample=$(mktemp --suffix=.png)
rendered=$(mktemp)
trap 'rm -f -- "$sample" "$rendered"' EXIT
base64 -d > "$sample" <<'PNG'
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=
PNG
catimg -r 1 -w 1 "$sample" > "$rendered"
test -s "$rendered"
grep -F $'\033[' "$rendered"
