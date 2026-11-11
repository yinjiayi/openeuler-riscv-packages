#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libcuckoo
rpm -V -- libcuckoo
printf '%s  %s\n' \
  cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 \
  /usr/share/licenses/libcuckoo/LICENSE-2.0.txt \
  8a79e0ec350fe0e029fdf9c27355cbe7e65511198e3e6fd10d839dfa41edb1ce \
  /usr/share/licenses/libcuckoo/LICENSE | sha256sum --check --strict
qa=/usr/share/libcuckoo/qa
test -d /usr/include/libcuckoo
test -d /usr/include/libcuckoo-c
test ! -e "$qa/source/libcuckoo"
test ! -e "$qa/source/libcuckoo-c"
test "$(rpm -qf --qf '%{NAME}\n' /usr/include/libcuckoo/cuckoohash_map.hh)" = libcuckoo
task_dir=$(mktemp -d /tmp/libcuckoo-installed.XXXXXXXX)
case "$task_dir" in /tmp/libcuckoo-installed.*) ;; *) exit 1 ;; esac
trap 'rm -rf -- "$task_dir"' EXIT
cmake -S "$qa" -B "$task_dir/build" -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_FLAGS='-O2 -UNDEBUG' -DCMAKE_CXX_FLAGS='-O2 -UNDEBUG' \
  -DCMAKE_FIND_USE_PACKAGE_REGISTRY=OFF -DCMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY=OFF
cmake --build "$task_dir/build" --parallel 2
ctest --test-dir "$task_dir/build" -N | grep -Fx 'Total Tests: 1'
ctest --test-dir "$task_dir/build" --output-on-failure --verbose
