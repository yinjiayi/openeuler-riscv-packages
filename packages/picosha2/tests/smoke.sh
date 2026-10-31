#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_defaults() {
    root="$1"
    work="$(mktemp -d)"
    mkdir "$work/test"
    cp "$root/usr/share/picosha2/qa/test.cpp" "$work/test/test.cpp"
    test -s "$work/test/test.cpp"
    ln -s "$root/usr/include/picosha2.h" "$work/picosha2.h"
    g++ -O2 -g -UNDEBUG "$work/test/test.cpp" -o "$work/unittest"
    (cd "$work/test" && "$work/unittest") > "$work/original.log" 2>&1
    cat "$work/original.log"
    test "$(grep -c ' is succeeded\.' "$work/original.log")" -eq 202
    ! grep -F ' is failed.' "$work/original.log"
}
run_installed_defaults ''
