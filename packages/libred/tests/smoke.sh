#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libred/qa/libred-1.1.3.tar.gz"
    echo '8d08527ae4892693bc9e1896f67c0d0538e46569bd3c9515f313e0f9c7a245fa  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libred.h" "$root/usr/include/libred.h"
    cd "$work"
    gcc -std=c99 -O2 -g -Wall -I"$root/usr/include" "$root/usr/share/libred/qa/consumer.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lred -lm -o consumer-shared
    readelf -d consumer-shared | grep 'Shared library: \[libred.so.1\]'
    gcc -std=c99 -O2 -g -Wall -I"$root/usr/include" "$root/usr/share/libred/qa/consumer.c" "$root/usr/lib64/libred.a" -lm -o consumer-static
    LD_LIBRARY_PATH="$root/usr/lib64" ./consumer-shared
    ./consumer-static
)
run_installed_tests ''
