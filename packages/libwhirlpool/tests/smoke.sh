#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libwhirlpool libwhirlpool-devel
rpm -V libwhirlpool libwhirlpool-devel
rpm -qf /usr/include/whirlpool.h /usr/lib64/libwhirlpool.so.0 /usr/lib64/libwhirlpool.a /usr/bin/whirlpoolsum
for name in COPYING GPL-2.0.txt GPL-3.0.txt APACHE-2.0.txt install-sh; do
    test -s "/usr/share/licenses/libwhirlpool/$name"
done
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
/usr/bin/whirlpoolsum --test > "$task_dir/upstream-api.log" 2>&1
cat "$task_dir/upstream-api.log"
grep -Fx 'No error detected.' "$task_dir/upstream-api.log"
if grep -F 'API error' "$task_dir/upstream-api.log"; then exit 1; fi
cd /usr/share/libwhirlpool/tests
sha256sum -c SHA256SUMS
fixture=$PWD/consumer.c
cd "$task_dir"
gcc -O2 "$fixture" -lwhirlpool -o installed-shared
readelf -d installed-shared | grep -F 'Shared library: [libwhirlpool.so.0]'
./installed-shared
gcc -O2 "$fixture" /usr/lib64/libwhirlpool.a -o installed-static
./installed-static
printf abc > input
whirlpoolsum input > checksum
grep -i '^4E2448A4C6F486BB16B6562C73B4020BF3043E3A731BCE721AE1B303D97E6D4C7181EEBDB6C57E277D0E34957114CBD6C797FC9D95D8B582D225292076D4EEF5 ' checksum
whirlpoolsum --check checksum | tee positive.log
grep -Fx 'input: OK' positive.log
printf changed > input
if whirlpoolsum --check checksum > negative.log 2>&1; then
    echo 'FAIL: changed input incorrectly accepted' >&2
    exit 1
else
    status=$?
    test "$status" -eq 1
fi
grep -Fx 'input: FAILED' negative.log
echo 'PASS downstream-libwhirlpool installed shared/static, CLI known vector and negative control; skips=0'
