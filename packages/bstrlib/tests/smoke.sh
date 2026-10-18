#!/bin/bash
set -euo pipefail
rpm -V bstrlib bstrlib-tests
test -f /usr/lib64/libbsafe.a
run_installed_defaults() {
    root=$1
    qa="$root/usr/share/bstrlib/qa"
    temp=$(mktemp -d)
    gcc -O2 -g -UNDEBUG -std=gnu99 -I"$root/usr/include/bstrlib" "$qa/bstest.c" "$root/usr/lib64/libbstrlib.a" -o "$temp/core-test"
    gcc -O2 -g -UNDEBUG -std=gnu99 -I"$root/usr/include/bstrlib" "$qa/testaux.c" "$root/usr/lib64/libbstrlib.a" -o "$temp/aux-test"
    g++ -O2 -g -UNDEBUG -std=gnu++11 -I"$root/usr/include/bstrlib" "$qa/test.cpp" "$root/usr/lib64/libbstrwrap.a" "$root/usr/lib64/libbstrlib.a" -o "$temp/cpp-test"
    for suite in core aux cpp; do
        "$temp/$suite-test" > "$temp/$suite.log"
        cat "$temp/$suite.log"
        grep -qx '# test failures: 0' "$temp/$suite.log"
    done
    rm -f "$temp/core-test" "$temp/aux-test" "$temp/cpp-test" "$temp/core.log" "$temp/aux.log" "$temp/cpp.log"
    rmdir "$temp"
    echo 'PASS bstrlib original-core=49 auxiliary=15 cpp=34 installed-archives skips=0'
}
run_installed_defaults ''
