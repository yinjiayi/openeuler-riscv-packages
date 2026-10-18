#!/bin/bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
unset CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH LIBRARY_PATH LD_PRELOAD
root=
if [[ ${1:-} == --staged ]]; then
    [[ $# == 2 && $2 == /* && -d $2/usr ]] || exit 2
    root=${2%/}
else
    [[ $# == 0 ]] || exit 2
    rpm -V tinycbor tinycbor-devel tinycbor-tests
fi
qa="$root/usr/share/tinycbor"
exe="$root/usr/libexec/tinycbor"
work=$(mktemp -d)
trap 'rm -r -- "$work"' EXIT
(cd "$exe" && sha256sum -c "$qa/SHA256SUMS")
count=0
for suite in c90 cpp encoder parser tojson; do
    "$exe/tst_$suite" > "$work/$suite.log" 2>&1 || { cat "$work/$suite.log"; exit 1; }
    cat "$work/$suite.log"
    count=$((count+1))
done
[[ $count == 5 ]]
printf 'original suite executables passed: %s\n' "$count"
# Preserve original data-row SKIP semantics; no zero-skip claim is made.
export PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="${root:-/}"
[[ $(pkg-config --modversion tinycbor) == 7.0 ]]
gcc -std=c99 -Wall -Wextra -Werror -UNDEBUG "$qa/consumer.c" \
    $(pkg-config --cflags --libs --static tinycbor) -o "$work/pkg-consumer"
"$work/pkg-consumer"
cmake -S "$qa" -B "$work/cmake" \
    -DCMAKE_PREFIX_PATH="$root/usr" \
    -DCMAKE_FIND_ROOT_PATH="$root" \
    -DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=ONLY
cmake --build "$work/cmake" --parallel 2
"$work/cmake/consumer"
printf '{"n":42,"ok":true}' > "$work/input.json"
"$exe/json2cbor" "$work/input.json" > "$work/data.cbor"
"$root/usr/bin/cbordump" -j "$work/data.cbor" > "$work/output.json"
printf '{"n":42,"ok":true}\n' > "$work/expected.json"
cmp "$work/expected.json" "$work/output.json"
printf 'downstream consumers passed: 2; CLI roundtrips passed: 1\n'
