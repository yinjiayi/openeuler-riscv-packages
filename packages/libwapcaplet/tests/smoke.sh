#!/bin/bash
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libwapcaplet/qa/libwapcaplet-0.4.3-src.tar.gz"
    echo '9b2aa1dd6d6645f8e992b3697fdbd87f0c0e1da5721fa54ed29b484d13160c5c  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    # Same predicate/message-preserving Check API port as all default suites.
    cp -- "$root/usr/share/libwapcaplet/qa/basictests.c" "$work/test/basictests.c"
    cmp -- "$work/include/libwapcaplet/libwapcaplet.h" "$root/usr/include/libwapcaplet/libwapcaplet.h"
    # Match the installed upstream-default release library; debug tests run separately.
    gcc -O2 -g -Wall -Werror -Wformat=2 -DNDEBUG -I"$root/usr/include" $(pkg-config --cflags check) "$work/test/testmain.c" "$work/test/basictests.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lwapcaplet $(pkg-config --libs check) -o "$work/shared-tests"
    readelf -d "$work/shared-tests" | grep 'Shared library: \[libwapcaplet.so.0\]'
    gcc -O2 -g -Wall -Werror -Wformat=2 -DNDEBUG -I"$root/usr/include" $(pkg-config --cflags check) "$work/test/testmain.c" "$work/test/basictests.c" "$root/usr/lib64/libwapcaplet.a" $(pkg-config --libs check) -o "$work/static-tests"
    LD_LIBRARY_PATH="$root/usr/lib64" "$work/shared-tests"
    "$work/static-tests"
    echo 'PASS libwapcaplet unchanged upstream release suite against installed shared and static libraries'
)
run_installed_tests ''
