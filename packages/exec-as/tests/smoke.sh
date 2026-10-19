#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    tool="$root/usr/bin/exec-as"
    archive="$root/usr/share/exec-as/qa/exec-as-1.2.3.tar.gz"
    echo '3813e2975216e3c332d69e6d9ff118efbf65eb3cabc87ea50cf33079540c5d44  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cd "$work"
    gcc -std=c99 -O2 -g -Wall -Wextra test.c -o original-test
    test "$("$tool" ./original-test 1 2 3)" = '1,3'
    test "$("$tool" ./original-test 'custom name' '' 'a b')" = 'custom name,3'
    test "$(PATH="$work:/usr/bin:/bin" "$tool" original-test custom)" = 'custom,1'
    test "$("$tool" /bin/sh custom -c 'printf "%s,%s\n" "$0" "$1"' 'two words')" = 'custom,two words'
    printf 'not executable\n' > denied
    chmod 600 denied
    expect_status() {
        expected=$1
        shift
        if "$@" > stdout.log 2> stderr.log; then actual=0; else actual=$?; fi
        test "$actual" -eq "$expected"
        test ! -s stdout.log
        test -s stderr.log
    }
    expect_status 125 "$tool"
    expect_status 127 "$tool" "$work/no-such-command" custom
    expect_status 126 "$tool" "$work/denied" custom
    expect_status 126 "$tool" "$work" custom
    if "$tool" /bin/sh custom -c 'exit 23'; then actual=0; else actual=$?; fi
    test "$actual" -eq 23
    echo 'PASS exec-as unchanged original driver, argv/PATH/status/error functional checks'
)
run_installed_tests ''
