#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- benchmark benchmark-devel
task_libdir=$(rpm --eval '%{_libdir}')
test -e "$task_libdir/libbenchmark.so.1"
test -e "$task_libdir/libbenchmark_main.so.1"
test -f /usr/include/benchmark/benchmark.h
