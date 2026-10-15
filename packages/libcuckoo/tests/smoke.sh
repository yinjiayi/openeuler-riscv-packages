#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libcuckoo
rpm -V -- libcuckoo
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
