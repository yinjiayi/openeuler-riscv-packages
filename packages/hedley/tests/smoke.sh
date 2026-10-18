#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
set -euo pipefail
export LC_ALL=C
unset CFLAGS CXXFLAGS MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEFILES
verify_default_outputs() {
    for name in array-param assume cast concat const constant deprecated empty-bases fallthrough flags inline likely malloc message noinline no-escape no-return non-null predict printf-format pure require restrict returns-non-null sentinel static-assert stringify unknown-cpp-attributes unknown-pragmas unavailable unreachable unused-function visibility warn warn-unused-result; do
        test -x "$1/$name" || return 1
        case "$name" in
            unknown-pragmas|unavailable|warn) test ! -e "$1/$name-cpp" || return 1 ;;
            *) test -x "$1/$name-cpp" || return 1 ;;
        esac
    done
    test "$(find "$1" -maxdepth 1 -type f -perm /111 | wc -l)" -eq 67
}
rpm -q hedley hedley-tests
rpm -V hedley hedley-tests
qa=$(mktemp -d)
trap 'find "$qa" -depth -delete' EXIT
cp /usr/include/hedley.h "$qa/"
cp -a /usr/share/hedley/qa/test "$qa/test"
make -C "$qa/test" all CC=gcc CXX=g++
verify_default_outputs "$qa/test"
echo 'PASS hedley installed-header=70 original-default final-files=67 compile-link-only'
