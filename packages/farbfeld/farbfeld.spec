# SPDX-License-Identifier: Apache-2.0
Name:           farbfeld
Version:        4
Release:        1%{?dist}
Summary:        Simple lossless image format and conversion tools
License:        ISC AND 0BSD
URL:            https://tools.suckless.org/farbfeld/
Source0:        farbfeld-4.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  python3
BuildRequires:  file
BuildRequires:  ImageMagick
Requires:       coreutils
Requires:       file
Requires:       ImageMagick

%description
Lossless farbfeld format and all upstream PNG, JPEG, PAM and PPM conversion
tools, including the original 2ff automatic conversion wrapper and fallback.

%package tests
Summary:        Offline conversion checks for farbfeld
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description tests
Downstream deterministic conversion and malformed-input checks. Upstream has
no check/test target. These are functional tests, not a security or fuzz audit.

%prep
%autosetup -n farbfeld-%{version}
# Add an original downstream checker without modifying any upstream file.
cat > downstream-check.py <<'FF_CHECK'
# SPDX-License-Identifier: ISC
import os
import pathlib
import struct
import subprocess
import sys
import zlib

assert not sys.flags.optimize
bindir = pathlib.Path(sys.argv[1]).resolve(strict=True)
env = dict(os.environ, PATH=str(bindir) + os.pathsep + os.environ['PATH'])
names = ('png2ff', 'ff2png', 'jpg2ff', 'ff2jpg', 'ff2pam', 'ff2ppm', '2ff')
assert all(os.access(bindir / n, os.X_OK) for n in names)

def run(name, data, args=(), good=True):
    q = subprocess.run([str(bindir / name), *args], input=data,
                       capture_output=True, env=env, timeout=30)
    if good:
        assert q.returncode == 0, (name, args, q.returncode, q.stderr)
    else:
        assert 0 < q.returncode < 256 and q.stderr, (name, q.returncode, q.stderr)
    return q.stdout

def ff(w, h, pixels):
    return b'farbfeld' + struct.pack('>II', w, h) + b''.join(
        struct.pack('>4H', *p) for p in pixels)

pixels = [(65535, 0, 0, 65535), (0, 12345, 65535, 0),
          (1234, 32768, 54321, 32768), (65535, 65535, 65535, 65535)]
data = ff(2, 2, pixels)
pam = b'P7\nWIDTH 2\nHEIGHT 2\nDEPTH 4\nMAXVAL 65535\nTUPLTYPE RGB_ALPHA\nENDHDR\n'
assert run('ff2pam', data) == pam + data[16:]
for args, mask in (((), (65535, 65535, 65535)),
                   (('-b', '000'), (0, 0, 0)),
                   (('-b', '00ff00'), (0, 65535, 0)),
                   (('-b', '0000ffff0000'), (0, 65535, 0))):
    expected = bytes((p[3] * p[c] + (65535 - p[3]) * mask[c]) // (65535 * 257)
                     for p in pixels for c in range(3))
    assert run('ff2ppm', data, args) == b'P6\n2 2\n255\n' + expected
print('PASS exact PAM, PPM and alpha-background formulas', flush=True)

png = run('ff2png', data)
assert png.startswith(b'\x89PNG\r\n\x1a\n') and run('png2ff', png) == data
def chunk(name, body):
    return struct.pack('>I', len(body)) + name + body + struct.pack(
        '>I', zlib.crc32(name + body))
raw8 = bytes((17, 34, 51, 68, 255, 0, 128, 255))
png8 = (b'\x89PNG\r\n\x1a\n' +
        chunk(b'IHDR', struct.pack('>IIBBBBB', 2, 1, 8, 6, 0, 0, 0)) +
        chunk(b'IDAT', zlib.compress(b'\0' + raw8)) + chunk(b'IEND', b''))
assert run('png2ff', png8) == ff(2, 1, [tuple(x * 257 for x in raw8[i:i+4])
                                      for i in (0, 4)])
print('PASS exact 16-bit PNG roundtrip and independent 8-bit PNG expansion', flush=True)

white = ff(8, 8, [(65535, 65535, 65535, 65535)] * 64)
for args in ((), ('-o', '-q', '100'), ('-b', '000', '-q', '90')):
    jpg = run('ff2jpg', white, args)
    assert jpg.startswith(b'\xff\xd8')
    back = run('jpg2ff', jpg)
    assert back[:16] == white[:16] and len(back) == len(white)
    values = struct.unpack('>256H', back[16:])
    assert all(values[i] == 65535 if i in range(3, 256, 4)
               else values[i] >= 250 * 257 for i in range(256))
print('PASS JPEG dimensions, opaque alpha and bounded lossy white conversion', flush=True)

assert run('2ff', data) == data
assert run('2ff', png) == data
# Exercise the retained ImageMagick fallback, not only built-in branches.
ppm = b'P6\n1 1\n255\n\xff\0\0'
assert run('2ff', ppm) == ff(1, 1, [(65535, 0, 0, 65535)])
print('PASS 2ff identity, PNG detection and ImageMagick PPM fallback', flush=True)

for name in names:
    run(name, b'', ('-invalid',), good=False)
for name in ('ff2pam', 'ff2ppm', 'ff2png', 'ff2jpg', 'png2ff', 'jpg2ff'):
    run(name, b'not-a-valid-image', good=False)
for name in ('ff2pam', 'ff2ppm', 'ff2png', 'ff2jpg'):
    run(name, data[:-1], good=False)
run('ff2jpg', data, ('-q', '101'), good=False)
run('ff2ppm', data, ('-b', 'zz'), good=False)
print('PASS invalid arguments, malformed/truncated image and option errors', flush=True)
print('PASS all five downstream conversion groups', flush=True)
FF_CHECK

%build
# Preserve upstream all and CPPFLAGS; allow RPM debug information.
make %{?_smp_mflags} CC='%{__cc}' CFLAGS='-std=c99 -pedantic -Wall -Wextra %{optflags}' LDFLAGS='%{?build_ldflags}'

%install
make install DESTDIR='%{buildroot}' PREFIX='%{_prefix}' MANPREFIX='%{_mandir}'
install -Dm644 downstream-check.py '%{buildroot}%{_datadir}/farbfeld/qa.py'

%check
# Upstream 4 has no original check/test target to skip or replace.
python3 -I -B downstream-check.py .
python3 -I -B '%{buildroot}%{_datadir}/farbfeld/qa.py' '%{buildroot}%{_bindir}'

%files
%license LICENSE
%doc README FORMAT
%{_bindir}/2ff
%{_bindir}/png2ff
%{_bindir}/ff2png
%{_bindir}/jpg2ff
%{_bindir}/ff2jpg
%{_bindir}/ff2pam
%{_bindir}/ff2ppm
%{_mandir}/man1/2ff.1*
%{_mandir}/man1/png2ff.1*
%{_mandir}/man1/ff2png.1*
%{_mandir}/man1/jpg2ff.1*
%{_mandir}/man1/ff2jpg.1*
%{_mandir}/man1/ff2pam.1*
%{_mandir}/man1/ff2ppm.1*
%{_mandir}/man5/farbfeld.5*

%files tests
%license LICENSE
%{_datadir}/farbfeld

%changelog
* Mon Oct 19 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4-1
- Retain all default converters and wrapper; add five offline check groups.
