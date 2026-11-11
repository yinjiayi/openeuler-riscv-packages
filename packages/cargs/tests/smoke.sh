#!/usr/bin/env bash
set -euo pipefail
rpm -q cargs cargs-tests
rpm -V cargs cargs-tests

run_installed_defaults() (
    root=$1
    qa=$root/usr/share/cargs/qa
    test -f "$root/usr/lib64/libcargs.a"
    export LC_ALL=C
    export PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig"
    export PKG_CONFIG_SYSROOT_DIR="$root"
    test "$(pkg-config --modversion cargs)" = 1.1.0
    test "$(pkg-config --variable=libdir cargs)" = "$root/usr/lib64"
    work=$(mktemp -d)
    cd "$work"
    # No source implementation is distributed with QA; link the installed .a.
    gcc -std=c11 -Wall -Wextra -Werror -Wpedantic $(pkg-config --cflags cargs) "$qa/main.c" "$qa/option_test.c" $(pkg-config --static --libs cargs) -o cargstest
    ./cargstest > all.log 2>&1
    cat all.log
    grep -Fx '23/23 (100.00%) of those tests succeeded.' all.log
    test "$(grep -Ec "^ Running 'option/.* SUCCESS$" all.log)" -eq 23
    # Replay every original registry entry as well, without modifying tests.h.
    grep -E '^  XX\(option,[a-z_]+\) ' "$qa/tests.h" > registry.txt
    test "$(wc -l < registry.txt)" -eq 23
    while IFS= read -r entry; do
        name=${entry#*XX(option,}
        name=${name%)*}
        ./cargstest option "$name" > "case-$name.log" 2>&1
        cat "case-$name.log"
        grep -Fx 'The test has been executed.' "case-$name.log"
        test "$(grep -Ec "^ Running 'option/.* SUCCESS$" "case-$name.log")" -eq 1
    done < registry.txt
    echo 'PASS cargs installed static library: all 23 original default cases'
)
run_installed_defaults ''
