#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- yyjson yyjson-devel
pkg-config --exists yyjson
python3 - <<'PY'
import ctypes

payload = b'{"isa":"RVA23","ok":true}'
source = ctypes.create_string_buffer(payload)
library = ctypes.CDLL("libyyjson.so.0")
library.yyjson_read_opts.argtypes = [
    ctypes.c_void_p,
    ctypes.c_size_t,
    ctypes.c_uint32,
    ctypes.c_void_p,
    ctypes.c_void_p,
]
library.yyjson_read_opts.restype = ctypes.c_void_p
library.yyjson_write_opts.argtypes = [
    ctypes.c_void_p,
    ctypes.c_uint32,
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_size_t),
    ctypes.c_void_p,
]
library.yyjson_write_opts.restype = ctypes.c_void_p

document = library.yyjson_read_opts(source, len(payload), 0, None, None)
if not document:
    raise SystemExit("yyjson failed to parse valid JSON")
output_length = ctypes.c_size_t()
output = library.yyjson_write_opts(document, 0, None, ctypes.byref(output_length), None)
if not output:
    raise SystemExit("yyjson failed to serialize the parsed document")
serialized = ctypes.string_at(output, output_length.value)
if serialized != payload:
    raise SystemExit(f"unexpected yyjson round trip: {serialized!r}")
PY
