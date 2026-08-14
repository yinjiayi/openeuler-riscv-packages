#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- html-xml-utils

workdir=$(mktemp -d)
trap 'rm -rf -- "$workdir"' EXIT

printf '<doc><item id="one">alpha</item><item id="two">beta</item></doc>\n' >"$workdir/input.xml"
hxnormalize -x "$workdir/input.xml" >"$workdir/normalized.xml"
hxselect -c 'item#two' <"$workdir/normalized.xml" >"$workdir/selected.txt"
grep -Fx 'beta' "$workdir/selected.txt"

printf 'caf\351\n' | asc2xml >"$workdir/utf8.txt"
printf 'caf\303\251\n' >"$workdir/expected-utf8.txt"
cmp -s "$workdir/expected-utf8.txt" "$workdir/utf8.txt"

xml2asc <"$workdir/expected-utf8.txt" >"$workdir/ascii.txt"
grep -Fx 'caf&#233;' "$workdir/ascii.txt"
asc2xml <"$workdir/ascii.txt" >"$workdir/roundtrip.txt"
cmp -s "$workdir/expected-utf8.txt" "$workdir/roundtrip.txt"
