#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libsha2/qa/libsha2-1.1.5.tar.gz"
    echo '7924ff2d6ac6ac3e8e8845db0c986b03cc7cad53a026cf382a0a15218d9daca1  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libsha2.h" "$root/usr/include/libsha2.h"
    test "$(grep -Ec '^[[:space:]]*test_repeated_huge\(' "$work/test.c")" = 16
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lsha2 -o "$work/test-shared"
    readelf -d "$work/test-shared" | grep 'Shared library: \[libsha2.so.1\]'
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" "$root/usr/lib64/libsha2.a" -o "$work/test-static"
    LD_LIBRARY_PATH="$root/usr/lib64" "$work/test-shared"
    "$work/test-static"
    echo 'PASS libsha2 complete original tests including all16 huge cases against installed shared and static libraries'
)
run_installed_tests ''
