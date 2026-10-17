#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libart-lgpl libart-lgpl-devel
python3 - <<'PY'
import ctypes

library = ctypes.CDLL("libart_lgpl_2.so.2")
version = tuple(
    ctypes.c_uint.in_dll(library, f"libart_{part}_version").value
    for part in ("major", "minor", "micro")
)
assert version == (2, 3, 21), version
matrix = (ctypes.c_double * 6)()
library.art_affine_identity.argtypes = [ctypes.POINTER(ctypes.c_double)]
library.art_affine_identity(matrix)
assert tuple(matrix) == (1.0, 0.0, 0.0, 1.0, 0.0, 0.0), tuple(matrix)
PY
test -f /usr/include/libart-2.0/libart_lgpl/art_affine.h
