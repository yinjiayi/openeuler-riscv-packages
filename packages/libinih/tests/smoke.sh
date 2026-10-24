#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail

rpm -q -- libinih libinih-devel
python3 - <<'PY'
import ctypes

library = ctypes.CDLL("libinih.so.0")
ctypes.CDLL("libINIReader.so.0")
entries = []
callback_type = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
)

@callback_type
def collect(_user, section, name, value):
    entries.append((section.decode(), name.decode(), value.decode()))
    return 1

library.ini_parse_string.argtypes = [ctypes.c_char_p, callback_type, ctypes.c_void_p]
library.ini_parse_string.restype = ctypes.c_int
status = library.ini_parse_string(b"[target]\narch=riscv64\n", collect, None)
assert status == 0, status
assert entries == [("target", "arch", "riscv64")], entries
PY
test -f /usr/include/ini.h
test -f /usr/include/INIReader.h
