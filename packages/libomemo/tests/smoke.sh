#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- libomemo
test -f /usr/include/libomemo/libomemo.h
test -e /usr/lib64/libomemo.so.0
test -f /usr/lib64/pkgconfig/libomemo.pc
grep -Fx 'Version: 0.8.1' /usr/lib64/pkgconfig/libomemo.pc
grep -Fx 'Requires.private: libgcrypt mxml4 sqlite3' /usr/lib64/pkgconfig/libomemo.pc
