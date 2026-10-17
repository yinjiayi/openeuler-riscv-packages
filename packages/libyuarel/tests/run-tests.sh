#!/usr/bin/bash
# SPDX-License-Identifier: MIT
set -euo pipefail
export LC_ALL=C
root=${1:-}
case "$root" in ''|/*) ;; *) echo 'root must be absolute' >&2; exit 2;; esac
data="$root/usr/share/libyuarel"
test -f "$root/usr/include/yuarel.h"
test -f "$root/usr/lib64/libyuarel.so.1"
test -L "$root/usr/lib64/libyuarel.so"
test "$(readlink "$root/usr/lib64/libyuarel.so")" = libyuarel.so.1
(cd "$data" && sha256sum -c SHA256SUMS)
temp=$(mktemp -d)
trap 'rm -rf -- "$temp"' EXIT
export LD_LIBRARY_PATH="$root/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
readelf -d "$root/usr/lib64/libyuarel.so.1" > "$temp/dynamic.txt"
grep -Fq '[libyuarel.so.1]' "$temp/dynamic.txt"
nm -D --defined-only "$root/usr/lib64/libyuarel.so.1" > "$temp/symbols.txt"
for symbol in yuarel_parse yuarel_split_path yuarel_parse_query; do
    grep -Eq "[[:space:]]T[[:space:]]${symbol}$" "$temp/symbols.txt"
done
gcc -std=gnu99 -O2 -Wall -I"$root/usr/include" "$data/tests/test_lib.c" -L"$root/usr/lib64" -lyuarel -o "$temp/upstream-tests"
"$temp/upstream-tests" > "$temp/upstream-tests.log"
cat "$temp/upstream-tests.log"
for group in 'yuarel_parse() with an HTTP URL' 'yuarel_parse() with faulty values' 'yuarel_split_path()' 'yuarel_parse_query()'; do
    grep -Fq "$group" "$temp/upstream-tests.log"
done
test "$(grep -Fc ' • yuarel_' "$temp/upstream-tests.log")" -eq 4
if grep -Fq '×' "$temp/upstream-tests.log"; then exit 1; fi
gcc -std=gnu99 -O2 -Wall -I"$root/usr/include" "$data/examples/simple.c" -L"$root/usr/lib64" -lyuarel -o "$temp/upstream-example"
"$temp/upstream-example" > "$temp/upstream-example.log"
cat "$temp/upstream-example.log"
grep -Fq "Path parts: 'path', 'to', 'test'" "$temp/upstream-example.log"
grep -Fq 'param1: no' "$temp/upstream-example.log"
grep -Fq 'query: yes' "$temp/upstream-example.log"
gcc -std=c99 -O2 -Wall -Wextra -Werror -I"$root/usr/include" "$data/consumer.c" -L"$root/usr/lib64" -lyuarel -o "$temp/downstream-consumer"
"$temp/downstream-consumer"
printf '%s\n' 'libyuarel: original four groups, original example, and downstream consumer passed'
