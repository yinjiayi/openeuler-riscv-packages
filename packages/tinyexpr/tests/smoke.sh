#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
run_installed_defaults() (
    root=$1
    test -f "$root/usr/include/tinyexpr.h"
    test -f "$root/usr/lib64/libtinyexpr.a"
    qa=$root/usr/share/tinyexpr/qa
    work=$(mktemp -d)
    cd "$work"
    # No implementation source is in QA: the original test links installed .a.
    gcc -Wall -Wshadow -O2 -I"$root/usr/include" "$qa/smoke.c" "$root/usr/lib64/libtinyexpr.a" -lm -o smoke
    ./smoke > original-default.log 2>&1
    cat original-default.log
    test "$(grep -Ec '^ALL TESTS PASSED \([0-9]+/[0-9]+\)$' original-default.log)" -eq 1
    test "$(grep -Ec '^[[:space:]]*(Results|Syntax|NaNs|INFs|Variables|Functions|Dynamic|Closure|Optimize|Pow|Combinatorics|Logic|Depth|Number|Locale)[[:space:]]+pass:' original-default.log)" -eq 15
    if grep -Ei 'skipping|SOME TESTS FAILED|FAILED:' original-default.log; then exit 1; fi
    echo 'PASS tinyexpr installed static archive: all 15 original default groups'
)
run_installed_defaults ''
