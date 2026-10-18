#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libnsgif/qa/libnsgif-1.0.0-src.tar.gz"
    echo '6014c842f61454d2f5a0f8243d7a8d7bde9b7da3ccfdca2d346c7c0b2c4c061b  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/include/nsgif.h" "$root/usr/include/nsgif.h"
    mkdir "$work/shared" "$work/static"
    gcc -O2 -g -DNSGIF_NAME=nsgif -DNSGIF_VERSION=1.0.0 -I"$root/usr/include" "$work/test/nsgif.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lnsgif -lm -o "$work/shared/test_nsgif"
    readelf -d "$work/shared/test_nsgif" | grep 'Shared library: \[libnsgif.so.1\]'
    gcc -O2 -g -DNSGIF_NAME=nsgif -DNSGIF_VERSION=1.0.0 -I"$root/usr/include" "$work/test/nsgif.c" "$root/usr/lib64/libnsgif.a" -lm -o "$work/static/test_nsgif"
    cd "$work"
    LD_LIBRARY_PATH="$root/usr/lib64" sh test/runtest.sh "$work/shared" > shared-summary.log
    cat shared-summary.log "$work/shared/test.log"
    grep -E '^Tests:[1-9][0-9]* Pass:[0-9]+ Fail:[0-9]+ Error:0$' shared-summary.log
    sh test/runtest.sh "$work/static" > static-summary.log
    cat static-summary.log "$work/static/test.log"
    grep -E '^Tests:[1-9][0-9]* Pass:[0-9]+ Fail:[0-9]+ Error:0$' static-summary.log
    echo 'PASS libnsgif full unchanged corpus script against installed shared and static libraries'
)
run_installed_tests ''
