# SPDX-License-Identifier: MIT
Name:           clipnotify
Version:        1.0.2
Release:        1%{?dist}
Summary:        Notify on X selection changes
License:        LicenseRef-clipnotify-public-domain
URL:            https://github.com/cdown/clipnotify
Source0:        https://codeload.github.com/cdown/clipnotify/tar.gz/22f7cb09d0b99af0aae7109aaff73760ef2dd5e3#/clipnotify-1.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libX11-devel
BuildRequires:  libXfixes-devel
BuildRequires:  python3
BuildRequires:  xorg-x11-server-Xvfb
ExclusiveArch:  riscv64

%description
Clipnotify waits for a change to the X PRIMARY or CLIPBOARD selection owner.
It emits no clipboard contents and exits when the original XFixes event arrives.
The exact upstream public-domain permission notice is retained unchanged.

%package tests
Summary:        Offline semantic checks for clipnotify
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       libXfixes
Requires:       xorg-x11-server-Xvfb
Requires:       bash
BuildArch:      noarch

%description tests
Mandatory built, staged and installed selection-notification checks using a
private Xvfb and independent Xlib ownership changes. Upstream has no test target.

%prep
%autosetup -n clipnotify-22f7cb09d0b99af0aae7109aaff73760ef2dd5e3
cat > downstream-qa.py <<'CLIPNOTIFY_QA'
#!/usr/bin/python3
"""Target-only mandatory selection-event checks; never run on intake host."""
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
    env.pop('DISPLAY', None)
    p = subprocess.run([binary], env=env, capture_output=True, timeout=10)
    assert (p.returncode, p.stdout, p.stderr) == (1, b'', b"Can't open X display\n")
    xvfb = shutil.which('Xvfb')
    assert xvfb, 'private Xvfb is mandatory, never skip'
    with tempfile.TemporaryDirectory(prefix='clipnotify-qa-') as temp:
        rd, wr = os.pipe()
        server = display = child = None
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
            fixes = C.CDLL('libXfixes.so.3')
            ptr, ulong = C.c_void_p, C.c_ulong

            def bind(obj, name, args, result):
                fn = getattr(obj, name)
                fn.argtypes, fn.restype = args, result
                return fn

            opend = bind(lib, 'XOpenDisplay', [C.c_char_p], ptr)
            close = bind(lib, 'XCloseDisplay', [ptr], C.c_int)
            root = bind(lib, 'XDefaultRootWindow', [ptr], ulong)
            intern = bind(lib, 'XInternAtom', [ptr, C.c_char_p, C.c_int], ulong)
            sync = bind(lib, 'XSync', [ptr, C.c_int], C.c_int)
            create = bind(lib, 'XCreateSimpleWindow',
                          [ptr, ulong, C.c_int, C.c_int, C.c_uint, C.c_uint,
                           C.c_uint, ulong, ulong], ulong)
            destroy = bind(lib, 'XDestroyWindow', [ptr, ulong], C.c_int)
            owner = bind(lib, 'XSetSelectionOwner', [ptr, ulong, ulong, ulong], C.c_int)
            getowner = bind(lib, 'XGetSelectionOwner', [ptr, ulong], ulong)
            query = bind(fixes, 'XFixesQueryExtension',
                         [ptr, C.POINTER(C.c_int), C.POINTER(C.c_int)], C.c_int)
            display = opend(env['DISPLAY'].encode('ascii'))
            assert display, 'cannot connect to our private Xvfb'
            event_base, error_base = C.c_int(), C.c_int()
            assert query(display, C.byref(event_base), C.byref(error_base)), 'XFIXES mandatory'
            windows = [create(display, root(display), 0, 0, 1, 1, 0, 0, 0) for _ in range(2)]
            assert all(windows) and len(set(windows)) == 2
            # Precreate CLIPBOARD exactly as upstream does; PRIMARY is predefined.
            clipboard = intern(display, b'CLIPBOARD', 0)
            primary = intern(display, b'PRIMARY', 0)
            assert primary == 1 and clipboard != primary
            sync(display, 0)
            for selection in (primary, clipboard):
                owner(display, selection, windows[0], 0)
                sync(display, 0)
                assert getowner(display, selection) == windows[0]
                child = subprocess.Popen([binary], env=env, stdin=subprocess.DEVNULL,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                deadline = time.monotonic() + 10
                changes = 0
                # Repeated *different owner* events deliberately avoid a startup
                # race with the original XFixes subscription. This is bounded
                # semantic workload, not a test retry or a timing benchmark.
                while child.poll() is None:
                    assert time.monotonic() < deadline, 'selection notification timeout'
                    win = windows[1 - (changes & 1)]
                    owner(display, selection, win, 0)
                    sync(display, 0)
                    assert getowner(display, selection) == win
                    changes += 1
                    time.sleep(0.02)
                out, err = child.communicate(timeout=5)
                assert changes > 0
                assert (child.returncode, out, err) == (0, b'', b''), (child.returncode, out, err)
                child = None
                assert server.poll() is None
            for win in windows:
                destroy(display, win)
            sync(display, 0)
        finally:
            if child is not None:
                if child.poll() is None:
                    child.kill()
                child.communicate(timeout=5)
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
CLIPNOTIFY_QA
cat > downstream-smoke.sh <<'CLIPNOTIFY_SMOKE'
#!/bin/bash
set -euo pipefail
test -x /usr/bin/clipnotify
test -f /usr/share/licenses/clipnotify/LICENSE
test -f /usr/share/licenses/clipnotify-tests/LICENSE
test -f /usr/share/doc/clipnotify/README.md
python3 -I -B /usr/libexec/clipnotify/qa.py /usr/bin/clipnotify
CLIPNOTIFY_SMOKE

%build
# Preserve original default all, caller flags, BSD search paths and X11/Xfixes.
%make_build CC=gcc CFLAGS='%{optflags}' LDFLAGS='%{?build_ldflags}'

%install
# Upstream has no install target; install only its binary and our mandatory QA.
install -Dpm 0755 clipnotify %{buildroot}%{_bindir}/clipnotify
install -Dpm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/clipnotify/qa.py
install -Dpm 0755 downstream-smoke.sh %{buildroot}%{_libexecdir}/clipnotify/smoke.sh

%check
python3 -I -B downstream-qa.py ./clipnotify
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/clipnotify

%files
%license LICENSE
%doc README.md
%{_bindir}/clipnotify

%files tests
%license LICENSE
%{_libexecdir}/clipnotify

%changelog
* Tue Oct 20 2026 openEuler RISC-V Packaging <noreply@example.invalid> - 1.0.2-1
- Preserve original defaults and require private-Xvfb semantic selection checks.
