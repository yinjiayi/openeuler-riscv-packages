#!/bin/bash
set -euo pipefail
rpm -V libfixmath libfixmath-tests
run_installed_defaults() {
    root=$1
    qa="$root/usr/share/libfixmath/qa"
    temp=$(mktemp -d)
    gcc -O2 -g -UNDEBUG -std=c11 -DPREFIX=ro64 -fsanitize=undefined -I"$root/usr/include" "$qa"/*.c "$root/usr/lib64/liblibfixmath.a" -lm -o "$temp/default-tests"
    "$temp/default-tests" > "$temp/default.log" 2>&1
    cat "$temp/default.log"
    if grep -E 'FAILED:|runtime error:|AddressSanitizer:|UndefinedBehaviorSanitizer:' "$temp/default.log"; then exit 1; fi
    for group in abs add mul div sub sqrt lerp macros; do
        grep -F "test_$group()" "$temp/default.log"
    done
    rm -f "$temp/default-tests" "$temp/default.log"
    rmdir "$temp"
    echo 'PASS libfixmath original-default=8 groups installed-static-archive skips=0'
}
run_installed_defaults ''
