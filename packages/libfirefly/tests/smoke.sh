#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libfirefly
rpm -V libfirefly
test "$(rpm -q --qf '%{ARCH}' libfirefly)" = riscv64
test "$(rpm -qf --qf '%{NAME}' /usr/include/firefly/vector.hpp)" = libfirefly
test "$(rpm -qf --qf '%{NAME}' /usr/include/firefly/utilities.hpp)" = libfirefly
workdir=$(mktemp -d)
trap 'rm -rf -- "$workdir"' EXIT
(cd /usr/share/libfirefly/tests && sha256sum -c SHA256SUMS.original)
cmp /usr/include/firefly/vector.hpp /usr/share/libfirefly/tests/headers/firefly/vector.hpp
cmp /usr/include/firefly/utilities.hpp /usr/share/libfirefly/tests/headers/firefly/utilities.hpp
env -u GTEST_FILTER -u GTEST_TOTAL_SHARDS -u GTEST_SHARD_INDEX -u GTEST_REPEAT \
  -u GTEST_SHUFFLE -u GTEST_FAIL_FAST -u GTEST_OUTPUT \
  /usr/libexec/libfirefly/FireflyTests --gtest_filter='*' --gtest_repeat=1 > "$workdir/original-tests.log"
cat "$workdir/original-tests.log"
grep -F '[  PASSED  ] 96 tests.' "$workdir/original-tests.log"
if grep -F '[  SKIPPED ]' "$workdir/original-tests.log"; then exit 1; fi
/usr/libexec/libfirefly/firefly-example
g++ -std=c++23 -O2 -UNDEBUG /usr/share/libfirefly/tests/verify-vector.cpp -o "$workdir/verify-vector"
"$workdir/verify-vector"
