#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libcircle libcircle-devel
rpm -V -- libcircle libcircle-devel
for notice in COPYING lx_find_mpi.m4 ltsugar.m4; do
    rpm -ql libcircle | grep -E "/licenses/libcircle[^/]*/$notice$"
done
test "$(pkg-config --modversion libcircle)" = 0.3.0
test -f /usr/include/libcircle.h
test "$(readlink -f /usr/lib64/libcircle.so)" = /usr/lib64/libcircle.so.2.1.1
readelf -d /usr/lib64/libcircle.so.2.1.1 | grep -F 'Library soname: [libcircle.so.2]'
unset LD_LIBRARY_PATH
bash /usr/share/libcircle/tests/run-original-tests.sh
