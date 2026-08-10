#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- aml aml-devel
task_libdir=$(rpm --eval '%{_libdir}')
test -e "$task_libdir/libaml.so.1"
test -f /usr/include/aml1/aml.h
test -f "$task_libdir/pkgconfig/aml1.pc"
