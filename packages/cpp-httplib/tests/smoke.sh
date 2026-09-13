#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- cpp-httplib
task_libdir=$(rpm --eval '%{_libdir}')
task_version=$(rpm -q --qf '%{VERSION}' -- cpp-httplib)
grep -Fx "#define CPPHTTPLIB_VERSION \"${task_version}\"" /usr/include/httplib.h
test -f "$task_libdir/cmake/httplib/httplibConfig.cmake"
