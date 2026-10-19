#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
run_installed_tests() (
    set -eux
    root=$1
    tool="$root/usr/bin/timeprefix"
    archive="$root/usr/share/timeprefix/qa/timeprefix-3.1.2.tar.gz"
    echo 'c473c23d46ad44947de33a5dc4a8cda3331594fe2c927d6125cb8dfbc1c40585  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cd "$work"
    # Exactly the original check pipeline, using the staged/installed command.
    test "$(printf '%s\n' a b c d e | "$tool" | sed 's/[0-9]/0/g' | md5sum | tr -Cd '[:xdigit:]\n')" = '3f1efed82f846e18973bd016fe5aeba4'
    strip_prefix() {
        sed -E 's/^\[[0-9]{10,}\.[0-9]{4} [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC\] //'
    }
    printf 'first line\n\n spaces \t remain\n' > input
    { printf '%s\n' '--- Program started ---'; cat input; printf '%s\n' '--- Program exited ---'; } > expected
    "$tool" < input > actual 2> stderr.log
    test ! -s stderr.log
    strip_prefix < actual > stripped
    cmp -- expected stripped
    "$tool" -- < input > actual
    strip_prefix < actual > stripped
    cmp -- expected stripped
    printf '%05000d\n' 0 > input
    { printf '%s\n' '--- Program started ---'; cat input; printf '%s\n' '--- Program exited ---'; } > expected
    "$tool" < input > actual
    strip_prefix < actual > stripped
    cmp -- expected stripped
    printf '%s\n' '--- Program started ---' '--- Program exited ---' > expected
    "$tool" < /dev/null > actual
    strip_prefix < actual > stripped
    cmp -- expected stripped
    if "$tool" unexpected > stdout.log 2> stderr.log; then actual_status=0; else actual_status=$?; fi
    test "$actual_status" -eq 1
    test ! -s stdout.log
    test -s stderr.log
    echo 'PASS timeprefix original normalized pipeline and installed payload/usage formatting checks'
)
run_installed_tests ''
