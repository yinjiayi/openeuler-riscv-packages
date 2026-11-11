#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libtmx
test -s /usr/lib64/libtmx.a
test -s /usr/include/tmx.h
test -s /usr/lib/cmake/tmx/tmxConfig.cmake
bash /usr/share/libtmx/run-tests.sh
