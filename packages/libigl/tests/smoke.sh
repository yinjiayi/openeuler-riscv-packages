#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libigl
test -f /usr/include/igl/adjacency_list.h
test -f /usr/lib64/cmake/igl/libigl-config.cmake
