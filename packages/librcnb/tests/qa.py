# SPDX-License-Identifier: MIT
"""Downstream functional regressions, not invented upstream test counts."""
import ctypes as C
import os
import sys

library = os.path.realpath(sys.argv[1])
assert os.path.isfile(library)
lib = C.CDLL(library)
wp, bp = C.POINTER(C.c_wchar), C.POINTER(C.c_char)
class State(C.Structure):
    _fields_ = [('i', C.c_size_t), ('trailing_code', C.c_wchar * 4)]
lib.rcnb_encode.argtypes = [bp, C.c_size_t, wp]
lib.rcnb_encode.restype = C.c_size_t
lib.rcnb_decode.argtypes = [wp, C.c_size_t, bp]
lib.rcnb_decode.restype = C.c_ssize_t
lib.rcnb_init_decodestate.argtypes = [C.POINTER(State)]
lib.rcnb_decode_block.argtypes = [wp, C.c_size_t, bp, C.POINTER(State)]
lib.rcnb_decode_block.restype = C.c_ssize_t
lib.rcnb_decode_blockend.argtypes = [bp, C.POINTER(State)]
lib.rcnb_decode_blockend.restype = C.c_ssize_t
with open('/proc/self/maps', encoding='utf-8') as f:
    maps = {os.path.realpath(line.split()[-1]) for line in f if '/' in line}
assert library in maps, ('loaded-library', library)
print('RPM_LIBRARY_BINDING', library, flush=True)
count = 0
def roundtrip(data, widths=()):
    global count
    n = len(data)
    src, enc, out = C.create_string_buffer(data), C.create_unicode_buffer(2*n+8), C.create_string_buffer(n+32)
    m = lib.rcnb_encode(src, n, enc)
    assert m == 2*n and enc[m] == '\0'
    got = lib.rcnb_decode(enc, m, out)
    assert got == n and out.raw[:n] == data
    count += 1
    for width in widths:
        state, total = State(), 0
        lib.rcnb_init_decodestate(C.byref(state))
        for offset in range(0, m, width):
            p = C.cast(C.byref(enc, offset*C.sizeof(C.c_wchar)), wp)
            q = C.cast(C.byref(out, total), bp)
            got = lib.rcnb_decode_block(p, min(width,m-offset), q, C.byref(state))
            assert 0 <= got <= n-total
            total += got
        got = lib.rcnb_decode_blockend(C.cast(C.byref(out,total),bp), C.byref(state))
        assert got >= 0 and total+got == n and out.raw[:n] == data and state.i == 0
        count += 1
for b in range(256):
    roundtrip(bytes([b]))
lengths = list(range(1,18)) + [31,32,33,63,64,65,99,100,101,255,256,257,4095,4096,4097]
for n in lengths:
    roundtrip(bytes((i*73+19)%256 for i in range(n)), range(1,14))
roundtrip(b'')
bad, out = C.create_unicode_buffer('xxxx'), C.create_string_buffer(8)
assert lib.rcnb_decode(bad,4,out) == -1
count += 1
assert count == 706
print('PASS downstream-regressions',count,flush=True)
