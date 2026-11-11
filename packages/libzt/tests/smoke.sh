#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libzt libzt-devel
rpm -V libzt libzt-devel
rpm -qf /usr/lib64/libzt.so.1 /usr/lib64/libzt.a /usr/include/zt.h /usr/bin/libzt-test
test -s /usr/share/licenses/libzt/LICENSE
test -s /usr/share/licenses/libzt/GPL-3.0.txt
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
/usr/bin/libzt-test | tee "$task_dir/upstream.log"
grep -Fx 'libzt self-test successful' "$task_dir/upstream.log"
cd /usr/share/libzt/tests
sha256sum -c SHA256SUMS
fixture=$PWD/consumer.c
cd "$task_dir"
gcc -O2 -UNDEBUG "$fixture" -lzt -o installed-shared
readelf -d installed-shared | grep -F 'Shared library: [libzt.so.1]'
./installed-shared -v
gcc -O2 -UNDEBUG "$fixture" /usr/lib64/libzt.a -o installed-static
./installed-static -v
gcc -O2 -UNDEBUG -DNEGATIVE_CONTROL "$fixture" -lzt -o negative-control
if ./negative-control > negative.log 2>&1; then
    echo 'FAIL: deliberate false claim was accepted' >&2
    exit 1
else
    status=$?
    test "$status" -eq 1
fi
grep -F 'assertion failed because false is false' negative.log
echo 'PASS downstream-libzt shared/static consumers and negative control; skips=0'
