#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libzupt
test -f /usr/include/zupt.hpp
test -f /usr/include/zupt_cxx.h
test -f /usr/lib64/libzupt.so.1.0.6
test -f /usr/lib64/pkgconfig/libzupt.pc
