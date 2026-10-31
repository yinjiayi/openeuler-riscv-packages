# SPDX-License-Identifier: MIT
Name:           sprop
Version:        0.1
Release:        1%{?dist}
Summary:        Simple X string property utility
License:        MIT
URL:            https://tools.suckless.org/x/sprop/
Source0:        https://dl.suckless.org/tools/sprop-0.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libX11-devel
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  xorg-x11-server-Xvfb
ExclusiveArch:  riscv64

%description
Sprop prints or sets string properties on an X server. It preserves the
original command-line behavior, including requiring an X display for -v.

%package tests
Summary:        Offline semantic checks for sprop
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       xorg-x11-server-Xvfb
Requires:       bash
BuildArch:      noarch

%description tests
Mandatory built, staged and installed string-property checks using a private
Xvfb and independent Xlib property reads. Upstream has no test/check target.

%prep
%autosetup -n sprop-%{version}
cat > downstream-qa.py <<'SPROP_QA'
#!/usr/bin/python3
"""Target-only: real Xlib string-property checks on one private Xvfb.

Never execute this file on the intake host. No network/display borrowing.
"""
import ctypes as C
import os
from pathlib import Path
import select
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    binary = str(Path(sys.argv[1]).resolve(strict=True))
    env = dict(os.environ)
    # XOpenDisplay precedes even -v/usage in the original program.
    env.pop('DISPLAY', None)
    p = subprocess.run([binary, '-v'], env=env, capture_output=True, timeout=10)
    assert (p.returncode, p.stdout, p.stderr) == (1, b'', b'sprop: cannot open display\n')
    xvfb = shutil.which('Xvfb')
    assert xvfb, 'private Xvfb is mandatory, never skip'
    with tempfile.TemporaryDirectory(prefix='sprop-qa-') as temp:
        rd, wr = os.pipe()
        server = None
        display = None
        lib = None
        try:
            with open(Path(temp) / 'xvfb.log', 'wb') as log:
                server = subprocess.Popen(
                    [xvfb, '-displayfd', str(wr), '-screen', '0', '320x240x24',
                     '-nolisten', 'tcp', '-noreset'],
                    pass_fds=(wr,), stdin=subprocess.DEVNULL, stdout=log, stderr=log)
            os.close(wr)
            wr = None
            limit = time.monotonic() + 15
            token = b''
            while b'\n' not in token:
                assert server.poll() is None, Path(temp, 'xvfb.log').read_bytes()
                remaining = limit - time.monotonic()
                assert remaining > 0, 'private Xvfb displayfd timeout'
                assert select.select([rd], [], [], remaining)[0], 'displayfd not ready'
                part = os.read(rd, 64)
                assert part, 'displayfd EOF'
                token += part
                assert len(token) < 64
            assert token.endswith(b'\n') and token[:-1].isdigit()
            env['DISPLAY'] = ':' + token[:-1].decode('ascii')
            lib = C.CDLL('libX11.so.6')
            window = C.c_ulong
            atom = C.c_ulong
            ptr = C.c_void_p
            byteptr = C.POINTER(C.c_ubyte)

            def bind(name, args, result):
                fn = getattr(lib, name)
                fn.argtypes, fn.restype = args, result
                return fn

            opend = bind('XOpenDisplay', [C.c_char_p], ptr)
            close = bind('XCloseDisplay', [ptr], C.c_int)
            root = bind('XDefaultRootWindow', [ptr], window)
            intern = bind('XInternAtom', [ptr, C.c_char_p, C.c_int], atom)
            sync = bind('XSync', [ptr, C.c_int], C.c_int)
            change = bind('XChangeProperty', [ptr, window, atom, atom, C.c_int,
                                           C.c_int, byteptr, C.c_int], C.c_int)
            get = bind('XGetWindowProperty', [ptr, window, atom, C.c_long, C.c_long,
                       C.c_int, atom, C.POINTER(atom), C.POINTER(C.c_int),
                       C.POINTER(C.c_ulong), C.POINTER(C.c_ulong),
                       C.POINTER(byteptr)], C.c_int)
            free = bind('XFree', [ptr], C.c_int)
            display = opend(env['DISPLAY'].encode())
            assert display, 'cannot connect to our private Xvfb'
            win = root(display)
            # The source uses only_if_exists=True; explicitly precreate both atoms.
            utf8 = intern(display, b'UTF8_STRING', 0)
            prop = intern(display, b'_SPROP_PACKAGE_QA', 0)
            assert utf8 and prop and win
            sync(display, 0)

            def invoke(args, code, stdout, stderr=b''):
                p = subprocess.run([binary] + args, env=env, capture_output=True, timeout=10)
                assert (p.returncode, p.stdout, p.stderr) == (code, stdout, stderr), (
                    args, p.returncode, p.stdout, p.stderr)

            invoke(['-v'], 0, 'sprop-0.1, © 2010 Connor Lane Smith\n'.encode())
            usage = b'usage: sprop <xid> <atom> [<value>] [-v]\n'
            for args in ([], ['-h'], ['-x'], ['1', 'a', 'b', 'extra']):
                invoke(args, 1, b'', usage)
            xid = str(win)  # Original atol accepts decimal, not an 0x hexadecimal XID.
            name = '_SPROP_PACKAGE_QA'

            def independent_read():
                actual, fmt = atom(), C.c_int()
                count, remaining = C.c_ulong(), C.c_ulong()
                data = byteptr()
                assert get(display, win, prop, 0, 65536, 0, utf8,
                           C.byref(actual), C.byref(fmt), C.byref(count),
                           C.byref(remaining), C.byref(data)) == 0
                try:
                    assert (actual.value, fmt.value, remaining.value) == (utf8, 8, 0)
                    return C.string_at(data, count.value)
                finally:
                    if data:
                        free(C.cast(data, ptr))

            # Set via original CLI; verify actual server type, format, length, bytes.
            for value in ('plain', 'spaces and -literal', 'héllo 世界', '', 'a\nb', 'x' * 8192):
                invoke([xid, name, value], 0, b'')
                sync(display, 0)
                assert independent_read() == value.encode()
                invoke([xid, name], 0, value.encode() + b'\n')

            # Seed independently with Xlib, then test original get path.
            value = b'independent Xlib seed'
            buf = C.create_string_buffer(value)
            change(display, win, prop, utf8, 8, 0, C.cast(buf, byteptr), len(value))
            sync(display, 0)
            invoke([xid, name], 0, value + b'\n')
            assert independent_read() == value
            assert server.poll() is None
        finally:
            if display:
                close(display)
            os.close(rd)
            if wr is not None:
                os.close(wr)
            if server is not None and server.poll() is None:
                server.terminate()
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)


if __name__ == '__main__':
    main()
SPROP_QA
cat > downstream-smoke.sh <<'SPROP_SMOKE'
#!/bin/bash
set -euo pipefail
test -x /usr/bin/sprop
test -f /usr/share/licenses/sprop/LICENSE
test -f /usr/share/licenses/sprop-tests/LICENSE
test -f /usr/share/doc/sprop/README
test -f /usr/share/man/man1/sprop.1.gz -o -f /usr/share/man/man1/sprop.1
python3 -I -B /usr/libexec/sprop/qa.py /usr/bin/sprop
SPROP_SMOKE

%build
# Keep original all/options, C99, pedantic, Wall, VERSION, libc and Xlib.
# Distribution flags replace original -Os/-s; install/X11 prefix follows distro.
%make_build CC=gcc PREFIX=%{_prefix} MANPREFIX=%{_mandir} \
 CFLAGS='%{optflags} -std=c99 -pedantic -Wall -I. -I/usr/include -DVERSION=\"0.1\"' \
 LDFLAGS='%{?build_ldflags} -L%{_libdir} -lc -lX11'

%install
%make_install CC=gcc PREFIX=%{_prefix} MANPREFIX=%{_mandir} \
 CFLAGS='%{optflags} -std=c99 -pedantic -Wall -I. -I/usr/include -DVERSION=\"0.1\"' \
 LDFLAGS='%{?build_ldflags} -L%{_libdir} -lc -lX11'
install -Dpm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/sprop/qa.py
install -Dpm 0755 downstream-smoke.sh %{buildroot}%{_libexecdir}/sprop/smoke.sh

%check
python3 -I -B downstream-qa.py ./sprop
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/sprop

%files
%license LICENSE
%doc README
%{_bindir}/sprop
%{_mandir}/man1/sprop.1*

%files tests
%license LICENSE
%{_libexecdir}/sprop

%changelog
* Mon Oct 19 2026 openEuler RISC-V Packaging <noreply@example.invalid> - 0.1-1
- Preserve original defaults and add offline semantic QA with mandatory private-Xvfb checks.
