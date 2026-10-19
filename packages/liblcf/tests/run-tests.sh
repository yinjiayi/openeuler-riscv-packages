#!/bin/bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
prefix=${1:-}
qa="$prefix/usr/share/liblcf"
lib="$prefix/usr/lib64"
(cd "$qa"; sha256sum -c SHA256SUMS)
test -f "$lib/liblcf.so.0"
test "$(readlink "$lib/liblcf.so")" = liblcf.so.0
readelf -d "$lib/liblcf.so.0" | grep -E 'SONAME.*liblcf\.so\.0' >/dev/null
test -f "$prefix/usr/share/mime/packages/liblcf.xml"
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
export LD_LIBRARY_PATH="$lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PKG_CONFIG_LIBDIR="$lib/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="$prefix"
test "$(pkg-config --modversion liblcf)" = 0.8.1
cp -R "$qa/." "$tmp/"
cmake -S "$tmp" -B "$tmp/build" -DCMAKE_BUILD_TYPE=RelWithDebInfo -Dliblcf_DIR="$lib/cmake/liblcf"
cmake --build "$tmp/build" --parallel 2
"$tmp/build/installed_originals" --no-colors > "$tmp/original-tests.log" 2>&1
cat "$tmp/original-tests.log"
grep -E 'test cases:.*[1-9][0-9]*.*passed.*0 failed' "$tmp/original-tests.log" >/dev/null
grep -E 'test cases:.*0 failed.*0 skipped' "$tmp/original-tests.log" >/dev/null
grep -E 'assertions:.*[1-9][0-9]*.*passed.*0 failed' "$tmp/original-tests.log" >/dev/null
(cd "$tmp"; ./build/installed_consumer)
g++ -std=c++17 -O2 -UNDEBUG -Wall "$qa/consumer.cpp" $(pkg-config --cflags --libs liblcf) -o "$tmp/pkg-consumer"
(cd "$tmp"; ./pkg-consumer)
rc=0; "$prefix/usr/bin/lcfstrings" --help > "$tmp/strings-help" 2>&1 || rc=$?
test "$rc" -eq 2
grep -F 'lcfstrings - Extract all strings' "$tmp/strings-help" >/dev/null
rc=0; "$prefix/usr/bin/lcf2xml" > "$tmp/xml-help" 2>&1 || rc=$?
test "$rc" -eq 1
grep -F 'LCF2XML - Converts' "$tmp/xml-help" >/dev/null
(cd "$tmp"; "$prefix/usr/bin/lcf2xml" sample.lmu)
test -s "$tmp/sample.emu"
"$prefix/usr/bin/lcfstrings" "$tmp/sample.lmu" > "$tmp/strings.txt"
printf 'liblcf installed checks passed: original_units=10 consumers=2 default_features=INI,ICU,XML tools=2\n'
