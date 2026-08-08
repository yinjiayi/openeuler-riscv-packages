#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- inih inih-devel
task_libdir=$(rpm --eval '%{_libdir}')
test -e "$task_libdir/libinih.so.0"
test -e "$task_libdir/libINIReader.so.0"
test -f /usr/include/ini.h
test -f /usr/include/INIReader.h
