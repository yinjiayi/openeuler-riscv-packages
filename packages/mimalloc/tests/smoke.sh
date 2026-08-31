#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- mimalloc mimalloc-devel mimalloc-static
test -r /usr/include/mimalloc.h
test -r /usr/lib64/libmimalloc.so.3
test -r /usr/lib64/libmimalloc.a
test -r /usr/lib64/pkgconfig/mimalloc.pc
grep -F 'Version: 3.5' /usr/lib64/pkgconfig/mimalloc.pc
