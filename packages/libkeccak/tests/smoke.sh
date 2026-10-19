#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libkeccak/qa/libkeccak-1.4.3.tar.gz"
    echo 'e395732342c9a6cbc22d709434a9d7b40f7b958952e9061ec09ec6d80d7ce83f  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libkeccak.h" "$root/usr/include/libkeccak.h"
    for header in keccak sha3 rawshake shake cshake extra hmac legacy util; do
        cmp -- "$work/libkeccak/$header.h" "$root/usr/include/libkeccak/$header.h"
    done
    cd "$work"
    echo 'e21d814d21ca269246849cc105faec1a71ac7d1cdb1a86023254f49d51b47231  .testfile' | sha256sum -c -
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lkeccak -o test-shared
    readelf -d test-shared | grep 'Shared library: \[libkeccak.so.1\]'
    gcc -std=c99 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -O2 -g -Wall test.c "$root/usr/lib64/libkeccak.a" -o test-static
    LD_LIBRARY_PATH="$root/usr/lib64" ./test-shared > shared.log
    cat shared.log
    if grep -F 'Fail' shared.log; then exit 1; fi
    ./test-static > static.log
    cat static.log
    if grep -F 'Fail' static.log; then exit 1; fi
    echo 'PASS libkeccak complete original eight-group driver against installed shared and static libraries'
)
run_installed_tests ''
