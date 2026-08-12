#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cpp-httplib
task_libdir=$(rpm --eval '%{_libdir}')
grep -F '#define CPPHTTPLIB_VERSION "0.53.0"' /usr/include/httplib.h
test -f "$task_libdir/cmake/httplib/httplibConfig.cmake"
