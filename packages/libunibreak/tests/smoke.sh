#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libunibreak libunibreak-devel
task_libdir=$(rpm --eval '%{_libdir}')
test -e "$task_libdir/libunibreak.so.7"
test -f /usr/include/linebreak.h
test -f /usr/include/wordbreak.h
test -f /usr/include/graphemebreak.h
