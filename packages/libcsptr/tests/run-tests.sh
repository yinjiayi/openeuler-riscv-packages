#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
root=
if [[ ${1:-} == --staged && $# == 2 ]]; then
    root=$2
elif [[ $# != 0 ]]; then
    printf '%s\n' 'usage: run-tests.sh [--staged ROOT]' >&2
    exit 2
fi
prefix="$root/usr"
base="$prefix/share/libcsptr/tests"
if [[ -z $root ]]; then
    test "$(rpm -q --qf '%{ARCH}' libcsptr)" = riscv64
    rpm -V libcsptr libcsptr-tests
fi
test -f "$prefix/lib64/libcsptr.a"
for h in config.h smalloc.h array.h smart_ptr.h common.h; do
    test -s "$prefix/include/csptr/$h"
done
pkg-config --exists check
(cd "$base/original"; sha256sum -c "$base/SHA256SUMS")
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
# Compile all original test bodies with modern Check registration against installed public API.
# Preserve all original GNU C compiler diagnostics and keep assertions enabled.
gcc -std=gnu99 -Wall -Wextra -Werror -g -Wno-unused-result \
    -Wno-missing-field-initializers -UNDEBUG \
    -I"$prefix/include" $(pkg-config --cflags check) \
    "$base/original/test.c" "$base/original/scalar.c" \
    "$base/original/array.c" "$base/original/shared.c" \
    "$base/original/misc.c" "$prefix/lib64/libcsptr.a" \
    $(pkg-config --libs check) -o "$work/check_unit"
"$work/check_unit" > "$work/original-check.log" 2>&1
cat "$work/original-check.log"
grep -F 'Checks: 12, Failures: 0, Errors: 0' "$work/original-check.log"
gcc -std=gnu99 -Wall -Wextra -Werror -g -Wno-unused-result \
    -Wno-missing-field-initializers -UNDEBUG -I"$prefix/include" \
    "$base/consumer.c" "$prefix/lib64/libcsptr.a" -o "$work/consumer"
"$work/consumer"
readelf -h "$work/consumer" | grep -E 'Machine:.*RISC-V'
printf '%s\n' 'PASS original Check cases=12 failures=0 errors=0 downstream shared-array regression=1 skips=0'
