#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libassert
test -f /usr/include/libassert/assert.hpp
test -f /usr/include/cpptrace/cpptrace.hpp
test -f /usr/lib64/cmake/libassert/libassert-config.cmake
test -f /usr/lib64/libassert.so.2.2.1
test -e /usr/lib64/libcpptrace.so
ldd /usr/lib64/libassert.so.2.2.1 | grep -F -- libcpptrace
