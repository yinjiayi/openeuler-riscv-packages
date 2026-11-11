#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q libgeneral libgeneral-devel
rpm -V libgeneral libgeneral-devel
rpm -qf /usr/lib64/libgeneral.so.0 /usr/lib64/libgeneral.a \
    /usr/include/libgeneral/Mem.hpp /usr/lib64/pkgconfig/libgeneral.pc
test -s /usr/share/licenses/libgeneral/LICENSE
test "$(pkg-config --modversion libgeneral)" = 90
pkg-config --validate libgeneral
fixture=/usr/share/libgeneral/tests
task_dir=$(mktemp -d)
trap 'rm -rf -- "$task_dir"' EXIT
cd "$fixture"
sha256sum -c SHA256SUMS
cd "$task_dir"
g++ -O2 -UNDEBUG -std=c++11 "$fixture/verify-general.cpp" \
    $(pkg-config --cflags --libs libgeneral) -o installed-shared
readelf -d installed-shared | grep -F 'Shared library: [libgeneral.so.0]'
library=$(ldd ./installed-shared | awk '$1 == "libgeneral.so.0" {print $3}')
test -n "$library"
rpm -qf "$(readlink -f "$library")"
./installed-shared
g++ -O2 -UNDEBUG -std=c++11 "$fixture/verify-general.cpp" \
    /usr/lib64/libgeneral.a -pthread -o installed-static
./installed-static
