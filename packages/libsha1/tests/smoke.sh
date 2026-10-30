#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libsha1/qa/libsha1-1.1.6.tar.gz"
    echo '55536baac47e1cc62ed33d87bbe1ffa42a96871c2d4e6c06ff81b7dc072d9318  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libsha1.h" "$root/usr/include/libsha1.h"
    test "$(grep -Ec '^[[:space:]]*test_repeated_huge\(' "$work/test.c")" = 4
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lsha1 -o "$work/test-shared"
    readelf -d "$work/test-shared" | grep 'Shared library: \[libsha1.so.1\]'
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall "$work/test.c" "$root/usr/lib64/libsha1.a" -o "$work/test-static"
    LD_LIBRARY_PATH="$root/usr/lib64" "$work/test-shared"
    "$work/test-static"
    echo 'PASS libsha1 complete original tests including four huge cases against installed shared and static libraries'
)
run_installed_tests ''
