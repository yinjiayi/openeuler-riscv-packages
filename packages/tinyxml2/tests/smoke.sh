#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- tinyxml2 tinyxml2-devel
task_libdir=$(rpm --eval '%{_libdir}')
test -e "$task_libdir/libtinyxml2.so.11"
test -f /usr/include/tinyxml2.h
test -f "$task_libdir/pkgconfig/tinyxml2.pc"
