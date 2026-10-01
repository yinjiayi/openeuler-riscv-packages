#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- cppitertools
test -f /usr/include/cppitertools/itertools.hpp
test -f /usr/share/cppitertools/cppitertools-config.cmake
