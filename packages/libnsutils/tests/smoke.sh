#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libnsutils/qa/libnsutils-0.1.1-src.tar.gz"
    echo '5694b4526e458ed000413ce6027589cbe10a257a7ecf065a01421dc7299dea92  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    for header in assert.h errors.h unistd.h endian.h base64.h time.h; do
        cmp -- "$work/include/nsutils/$header" "$root/usr/include/nsutils/$header"
    done
    test "$(grep -Ec '^b64(enctst|dectst|urlenctst|urldectst) ' "$work/test/runtest.sh")" = 32
    mkdir "$work/shared" "$work/static"
    gcc -O2 -g -I"$root/usr/include" "$work/test/base64.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lnsutils -o "$work/shared/test_base64"
    readelf -d "$work/shared/test_base64" | grep 'Shared library: \[libnsutils.so.0\]'
    gcc -O2 -g -I"$root/usr/include" "$work/test/base64.c" "$root/usr/lib64/libnsutils.a" -o "$work/static/test_base64"
    LD_LIBRARY_PATH="$root/usr/lib64" bash -eux "$work/test/runtest.sh" "$work/shared"
    bash -eux "$work/test/runtest.sh" "$work/static"
    echo 'PASS libnsutils unchanged 32-case script against installed shared and static libraries'
)
run_installed_tests ''
