#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- sparsehash
task_libdir=$(rpm --eval '%{_libdir}')
test -f /usr/include/sparsehash/dense_hash_map
test -f /usr/include/sparsehash/internal/sparseconfig.h
test -f /usr/include/google/dense_hash_map
test -f "$task_libdir/pkgconfig/libsparsehash.pc"
