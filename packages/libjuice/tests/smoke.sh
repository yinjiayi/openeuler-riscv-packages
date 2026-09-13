#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libjuice
test -f /usr/include/juice/juice.h
test -f /usr/lib64/libjuice.so.1.7.3
test -f /usr/lib64/cmake/LibJuice/LibJuiceConfig.cmake
