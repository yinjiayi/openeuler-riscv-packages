#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libabort/qa/libabort-1.0.tar.gz"
    echo '7ca1c0762ed7cf439f5d6d548bcc62b0dd0830edab26810b9ea0bbd2c7a4656f  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libabort.h" "$root/usr/include/libabort.h"
    cd "$work"
    for api in stracpy stpacpy stracat stralen stpacat saprintf vsaprintf; do
        gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DTEST -fno-inline -O2 -g -Wall "libabort_$api.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -labort -o "$api-shared"
        gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DTEST -fno-inline -O2 -g -Wall "libabort_$api.c" "$root/usr/lib64/libabort.a" -o "$api-static"
        LD_LIBRARY_PATH="$root/usr/lib64" "./$api-shared"
        "./$api-static"
        echo "PASS libabort original $api driver shared and static"
    done
    readelf -d stracpy-shared | grep 'Shared library: \[libabort.so.1\]'
    echo 'PASS libabort all seven original drivers against installed shared and static libraries'
)
run_installed_tests ''
