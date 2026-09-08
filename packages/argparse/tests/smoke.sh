#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- argparse
task_libdir=$(rpm --eval '%{_libdir}')
test -f /usr/include/argparse/argparse.hpp
test -f "$task_libdir/cmake/argparse/argparseConfig.cmake"
test -f "$task_libdir/pkgconfig/argparse.pc"
