# SPDX-License-Identifier: Apache-2.0
Name:           librcnb
Version:        1.0.0
Release:        1%{?dist}
Summary:        C and C++ library and command-line tools for RCNB encoding
License:        MIT
URL:            https://github.com/rcnbapp/librcnb
Source0:        librcnb-1.0.0.tar.gz
Patch0:         0001-consume-complete-decoder-quartet.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.1
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  python3

%description
C and C++ interfaces for encoding and decoding binary data as RCNB text.
Root MIT and the literal public-domain notices in original sources are retained.

%package devel
Summary:        Headers, static library, CMake export and original librcnb sources
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-tools%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       glibc-devel
Requires:       python3

%description devel
Development headers, the original default static library and shared-library
CMake export. Original example sources and literal license notices are retained
for checking the actual installed RPM-owned library.

%package tools
Summary:        Original rcnb command-line encoder and decoder
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
The original upstream rcnb command-line encoder and decoder, built by the
default CMake configuration. Its original CLI round-trip test is retained.

%prep
%autosetup -N -n librcnb-45dd2e77d3f06165c7f0511d9556b88b4497c0dc
mkdir upstream-originals
tar -xzf %{SOURCE0} -C upstream-originals --strip-components=1
cat > upstream-originals/EXAMPLE-SHA256SUMS <<'HASHES'
779cbe0ada71b0ae3003f63bd8af26d38da2537922a779ac5c9f826fc72335a0  c-example1.c
163e1ec713bd2e61a455902a8b4ccc3b30a79d07cfd4186e653da71734142e6f  c-example2.c
bb4953317619398b6a334b4f894d2fa6901f9eb69dd94af600b53a9e9b71a575  cpp-example3.cc
a818ee4f548475ad7bc61249da85b94d8c8424344c2aa3cd7a314cb9283bf1b7  cpp-rcnb-cli.cc
3b166d43d3bd268028559ba12b2ccdc0f689a05babf6feee2f49bacef0e353f5  python3-example.py
HASHES
(cd upstream-originals/examples && sha256sum -c ../EXAMPLE-SHA256SUMS)
%autopatch -p1
cat > qa.py <<'PY'
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
    roundtrip(bytes((i*73+19)%%256 for i in range(n)), range(1,14))
roundtrip(b'')
bad, out = C.create_unicode_buffer('xxxx'), C.create_string_buffer(8)
assert lib.rcnb_decode(bad,4,out) == -1
count += 1
assert count == 706
print('PASS downstream-regressions',count,flush=True)
PY

%build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS_RELEASE="%{optflags} -UNDEBUG" \
    -DCMAKE_CXX_FLAGS_RELEASE="%{optflags} -UNDEBUG" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib}
cmake --build build --parallel %{_smp_build_ncpus}
test -f build/librcnb-static.a
for name in example1 example2 example3 rcnb; do test -x build/$name; done

%install
DESTDIR=%{buildroot} cmake --install build
install -m 0644 build/librcnb-static.a %{buildroot}%{_libdir}/librcnb-static.a
install -Dm0755 build/rcnb %{buildroot}%{_bindir}/rcnb
install -d %{buildroot}%{_datadir}/librcnb/tests
cp -a upstream-originals %{buildroot}%{_datadir}/librcnb/
install -m 0644 qa.py %{buildroot}%{_datadir}/librcnb/tests/qa.py

%check
export LC_ALL=C.UTF-8
test "$(locale charmap)" = UTF-8
(cd upstream-originals/examples && sha256sum -c ../EXAMPLE-SHA256SUMS)
./build/example1
env LD_LIBRARY_PATH="$PWD/build" python3 upstream-originals/examples/python3-example.py > python-source.txt
grep -Fx 'The Quick Brown RC Jumps Over the NB Dog. 😄' python-source.txt
python3 qa.py "$PWD/build/librcnb.so.1"
mkdir source-tests
cd source-tests
echo "The Quick Brown RC Jumps Over the NB Dog." > in.txt
../build/rcnb -e in.txt out.rcnb
../build/rcnb -d out.rcnb out.txt
cmp in.txt out.txt
printf AB > two.txt
../build/rcnb -e two.txt two.rcnb
../build/rcnb -d two.rcnb two-out.txt
cmp two.txt two-out.txt
echo 'PASS original-source-appveyor-vector and exact-two-byte CLI regression'
cd ..
gcc %{optflags} -UNDEBUG -I%{buildroot}%{_includedir} \
    upstream-originals/examples/c-example1.c -L%{buildroot}%{_libdir} -lrcnb -o staged-example1
env LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./staged-example1
env LD_LIBRARY_PATH=%{buildroot}%{_libdir} python3 upstream-originals/examples/python3-example.py > python-staged.txt
grep -Fx 'The Quick Brown RC Jumps Over the NB Dog. 😄' python-staged.txt
python3 qa.py %{buildroot}%{_libdir}/librcnb.so.1

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README INSTALL
%{_libdir}/librcnb.so.1*

%files devel
%{_includedir}/rcnb/
%{_libdir}/librcnb.so
%{_libdir}/librcnb-static.a
%{_datadir}/librcnb/

%files tools
%{_bindir}/rcnb

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Pin official release, preserve all default targets and original CLI test.
- Consume complete decoder quartets; retain byte/chunk regressions for target CI.
