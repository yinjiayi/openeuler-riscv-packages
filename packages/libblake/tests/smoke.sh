#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libblake/qa/libblake-3.0.2.1.tar.gz"
    echo '6855dc9fb107d13764c9619deab482ec0f20064c140989bb6b6a936ac0cc3c4d  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libblake.h" "$root/usr/include/libblake.h"
    for kat in blake2s blake2b blake2xs blake2xb; do test -s "$work/kat/$kat"; done
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DSUPPORT_BLAKE224 -DSUPPORT_BLAKE256 -DSUPPORT_BLAKE384 -DSUPPORT_BLAKE512 -DSUPPORT_BLAKE2S -DSUPPORT_BLAKE2B -DSUPPORT_BLAKE2XS -DSUPPORT_BLAKE2XB -O2 -g -Wall "$work/test.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lblake -o "$work/test-shared"
    readelf -d "$work/test-shared" | grep 'Shared library: \[libblake.so.3\]'
    gcc -std=c11 -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -DSUPPORT_BLAKE224 -DSUPPORT_BLAKE256 -DSUPPORT_BLAKE384 -DSUPPORT_BLAKE512 -DSUPPORT_BLAKE2S -DSUPPORT_BLAKE2B -DSUPPORT_BLAKE2XS -DSUPPORT_BLAKE2XB -O2 -g -Wall "$work/test.c" "$root/usr/lib64/libblake.a" -o "$work/test-static"
    cd "$work"
    LD_LIBRARY_PATH="$root/usr/lib64" ./test-shared
    ./test-static
    echo 'PASS libblake complete original tests, all eight algorithms and four KAT files against installed shared and static libraries'
)
run_installed_tests ''
