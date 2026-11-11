#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
rpm -q greatest greatest-tests
rpm -V greatest greatest-tests
# The examples intentionally demonstrate failures and skips. Check exact
# default counts and exit codes; never turn an arbitrary failure into success.
run_expected() {
    name=$1 total=$2 passed=$3 failed=$4 skipped=$5 expected_rc=$6
    if "./$name" > "$name.log" 2>&1; then rc=0; else rc=$?; fi
    cat "$name.log"
    test "$rc" -eq "$expected_rc"
    test "$(grep -Ec "^Total: $total tests? " "$name.log")" -eq 1
    test "$(grep -Fxc "Pass: $passed, fail: $failed, skip: $skipped." "$name.log")" -eq 1
}
run_all_defaults() (
    cd "$1"
    unset CFLAGS CXXFLAGS CPPFLAGS LDFLAGS COMMON_FLAGS MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEFILES
    export LC_ALL=C
    make all all_cpp CC=gcc CXX=g++
    # An independent stdlib-only process observes this target libc's default
    # rand sequence. No greatest header, reseeding or symbol interposition.
    cat > rand-oracle.c <<'ORACLE'
#include <stdio.h>
#include <stdlib.h>
int main(void) {
    unsigned int i, pass = 9, fail = 20, skip = 2, total = 231;
#if !defined(__STDC_VERSION__) || __STDC_VERSION__ < 19901L
    pass--; fail--; total -= 2;
#endif
    for (i = 0; i < 200; i++) {
        int r = rand() % 10;
        if (r == 0) fail++;
        else if (r == 1) skip++;
        else pass++;
    }
    if (pass + fail + skip != total) return 2;
    printf("%u %u %u %u\n", total, pass, fail, skip);
    return 0;
}
ORACLE
    gcc -Wall -Wextra -pedantic -Werror rand-oracle.c -o rand-oracle
    ./rand-oracle > rand-expected.txt
    read -r total passed failed skipped < rand-expected.txt
    run_expected example "$total" "$passed" "$failed" "$skipped" 1
    run_expected example_no_suite 3 1 1 1 1
    run_expected example_no_runner 1 1 0 0 0
    run_expected example_shuffle 1066 1064 2 0 1
    run_expected example_trunc 11 11 0 0 0
    run_expected example_cpp 1 0 1 0 1
    grep -Fx 'pass 1, fail 0, skip 0, assertions 0' example_no_runner.log
    grep -Fx 'fib 39 -> 102334155' example.log
    echo 'PASS greatest six original default examples; exact counts and exits'
)

qa=$(mktemp -d)
# The disposable smoke container owns this exclusive source/build directory.
cp /usr/include/greatest.h "$qa/"
cp /usr/share/greatest/qa/* "$qa/"
run_all_defaults "$qa"
