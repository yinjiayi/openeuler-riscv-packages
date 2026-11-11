#!/bin/bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
prefix=${1:-}
qa="$prefix/usr/share/libjson"
lib="$prefix/usr/lib64"
include="$prefix/usr/include"
test -f "$include/json.h"
test -f "$lib/libjson.a"
test -f "$lib/libjson.so.0.8.0"
test "$(readlink "$lib/libjson.so")" = libjson.so.0
test "$(readlink "$lib/libjson.so.0")" = libjson.so.0.8
test "$(readlink "$lib/libjson.so.0.8")" = libjson.so.0.8.0
readelf -d "$lib/libjson.so.0.8.0" | grep -E 'SONAME.*libjson\.so\.0\.8\.0' >/dev/null
ar t "$lib/libjson.a" | grep -Fx json.o >/dev/null
(cd "$qa"; sha256sum -c SHA256SUMS)
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
export LD_LIBRARY_PATH="$lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PKG_CONFIG_LIBDIR="$lib/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="$prefix"
test "$(pkg-config --modversion libjson)" = 0.8
# The source copy is outside include/ so quoted json.h resolves to installed header.
gcc -std=gnu99 -O2 -Wall -I"$include" "$qa/jsonlint.c" -L"$lib" -ljson -o "$tmp/jsonlint"
gcc -std=c99 -O2 -Wall -Wextra "$qa/consumer.c" $(pkg-config --cflags --libs libjson) -o "$tmp/shared-consumer"
gcc -std=c99 -O2 -Wall -Wextra -I"$include" "$qa/consumer.c" "$lib/libjson.a" -o "$tmp/static-consumer"
"$tmp/shared-consumer"
"$tmp/static-consumer"
cp -R "$qa/tests" "$tmp/tests"
chmod +x "$tmp/tests/runtest"
# Keep original runner and fixtures byte-for-byte, but also enforce actual results.
(cd "$tmp/tests"; ./runtest) > "$tmp/original-tests.log" 2>&1
cat "$tmp/original-tests.log"
if grep -F FAILED "$tmp/original-tests.log"; then exit 1; fi
test "$(grep -c SUCCESS "$tmp/original-tests.log")" -eq 33
good=0; bad=0
for f in "$qa"/tests/good/*.json; do
    "$prefix/usr/bin/jsonlint" --verify "$f"
    "$tmp/jsonlint" --verify "$f"
    good=$((good+1))
done
for f in "$qa"/tests/bad/*.json; do
    for cli in "$prefix/usr/bin/jsonlint" "$tmp/jsonlint"; do
        rc=0
        "$cli" --verify "$f" || rc=$?
        test "$rc" -eq 1
    done
    bad=$((bad+1))
done
test "$good" -eq 21
test "$bad" -eq 12
printf '{"x":[1,true,false,null,"z"]}\n' > "$tmp/sample.json"
for cli in "$prefix/usr/bin/jsonlint" "$tmp/jsonlint"; do
    "$cli" --format "$tmp/sample.json" > "$tmp/formatted.json"
    "$cli" --verify "$tmp/formatted.json"
    "$cli" --tree "$tmp/sample.json" > "$tmp/tree.txt"
    test -s "$tmp/tree.txt"
done
printf 'libjson installed checks passed: original=33 good=21 bad=12 consumers=2\n'
