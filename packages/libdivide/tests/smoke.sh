#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libdivide
rpm -V -- libdivide
for notice in LICENSE.txt CC0-1.0.txt divlu.c; do
    rpm -ql libdivide | grep -E "/licenses/libdivide[^/]*/$notice$"
done
for header in libdivide.h constant_fast_div.h constant_fast_div.hpp s16_ldparams.h s16_ldparams.hpp u16_ldparams.h u16_ldparams.hpp; do
    test -f "/usr/include/$header"
done
test -f /usr/lib64/cmake/libdivide/libdivideConfig.cmake
test -f /usr/lib64/cmake/libdivide/libdivideConfigVersion.cmake
bash /usr/share/libdivide/tests/run-original-tests.sh
