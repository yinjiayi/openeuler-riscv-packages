#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$(rpm -q --qf '%{VERSION}' -- libtelnet)" = 0.23
test -f /usr/include/libtelnet.h
test -x /usr/libexec/libtelnet-tests/telnet-test
for program in telnet-client telnet-chatd telnet-proxy; do
    test -x "/usr/bin/$program"
done
cd /usr/share/libtelnet
sha256sum -c tests.sha256
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cp -a test "$work/test"
mkdir "$work/util"
ln -s /usr/libexec/libtelnet-tests/telnet-test "$work/util/telnet-test"
cd "$work/test"
# Run upstream's original suite and all 11 original fixtures against installed ELF.
./run-all.sh > "$work/results.log" 2>&1
cat "$work/results.log"
test "$(grep -c 'OK$' "$work/results.log")" -eq 11
! grep -q 'FAIL' "$work/results.log"
