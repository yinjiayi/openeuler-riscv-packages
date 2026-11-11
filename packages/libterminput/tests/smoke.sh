#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libterminput/qa/libterminput-1.1.2.tar.gz"
    echo '2757ca59bf4e08e63788e368eb340d9f4784b7aa3da965f35ea53be15acd0ffc  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libterminput.h" "$root/usr/include/libterminput.h"
    cd "$work"
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lterminput -o test-shared
    readelf -d test-shared | grep 'Shared library: \[libterminput.so.1\]'
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c "$root/usr/lib64/libterminput.a" -o test-static
    LD_LIBRARY_PATH="$root/usr/lib64" ./test-shared
    ./test-static
    echo 'PASS libterminput complete original pipe-based driver against installed shared and static libraries'
)
run_installed_tests ''
