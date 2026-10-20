# SPDX-License-Identifier: MIT
Name:           lemonbar
Version:        1.5
Release:        1%{?dist}
Summary:        Lightweight XCB status bar with text formatting and clickable areas
License:        MIT
URL:            https://github.com/LemonBoy/bar
Source0:        https://codeload.github.com/LemonBoy/bar/tar.gz/5420c86be097819028a9504c1cb6a8f7f23ab5c8#/lemonbar-1.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libxcb-devel
BuildRequires:  perl-podlators
BuildRequires:  python3
BuildRequires:  libX11
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-fonts
ExclusiveArch:  riscv64

%description
Lemonbar is a lightweight XCB status bar with UTF-8 text, formatting, clickable
areas and RandR monitor support. The default upstream build is preserved.
The official v1.5 tag retains upstream's internal VERSION=1.4 unchanged.

%package tests
Summary:        Offline semantic checks for lemonbar
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       xorg-x11-server-Xvfb
Requires:       xorg-x11-fonts
Requires:       bash
BuildArch:      noarch

%description tests
Mandatory private-Xvfb checks of real status-bar pixels, geometry, EWMH properties,
click output and EOF/permanent behavior. Upstream has no original test target.

%prep
%autosetup -n bar-5420c86be097819028a9504c1cb6a8f7f23ab5c8
cat > downstream-qa.py <<'LEMONBAR_QA'
#!/usr/bin/python3
"""Mandatory target-only semantic workload; never executed on intake host."""
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
    mode = sys.argv[2] if len(sys.argv) == 3 else 'default'
    assert mode in ('default', 'xinerama')
    env = dict(os.environ)
    env.pop('DISPLAY', None)
    failed = subprocess.run([binary, '-h'], env=env, capture_output=True, timeout=10)
    assert (failed.returncode, failed.stdout, failed.stderr) == (1, b'', b"Couldn't connect to X\n")
    xvfb = shutil.which('Xvfb')
    assert xvfb, 'private Xvfb is mandatory'
    with tempfile.TemporaryDirectory(prefix='lemonbar-qa-') as temp:
        rd, wr = os.pipe()
        server = display = child = None
        try:
            with open(Path(temp) / 'xvfb.log', 'wb') as log:
                server = subprocess.Popen([xvfb, '-displayfd', str(wr), '-screen', '0',
                    '320x240x24', '-nolisten', 'tcp', '-noreset'] +
                    (['+xinerama', '-extension', 'RANDR'] if mode == 'xinerama' else []), pass_fds=(wr,),
                    stdin=subprocess.DEVNULL, stdout=log, stderr=log)
            os.close(wr)
            wr = None
            deadline = time.monotonic() + 15
            token = b''
            while b'\n' not in token:
                assert server.poll() is None, Path(temp, 'xvfb.log').read_bytes()
                remaining = deadline - time.monotonic()
                assert remaining > 0 and select.select([rd], [], [], remaining)[0]
                data = os.read(rd, 64)
                assert data
                token += data
                assert len(token) < 64
            assert token.endswith(b'\n') and token[:-1].isdigit()
            env['DISPLAY'] = ':' + token[:-1].decode('ascii')
            lib = C.CDLL('libX11.so.6')
            ptr, ul, integer = C.c_void_p, C.c_ulong, C.c_int
            def bind(name, args, result):
                fn = getattr(lib, name)
                fn.argtypes, fn.restype = args, result
                return fn
            open_display = bind('XOpenDisplay', [C.c_char_p], ptr)
            close_display = bind('XCloseDisplay', [ptr], integer)
            root = bind('XDefaultRootWindow', [ptr], ul)
            sync = bind('XSync', [ptr, integer], integer)
            intern = bind('XInternAtom', [ptr, C.c_char_p, integer], ul)
            query_tree = bind('XQueryTree', [ptr, ul, C.POINTER(ul), C.POINTER(ul),
                C.POINTER(C.POINTER(ul)), C.POINTER(C.c_uint)], integer)
            free = bind('XFree', [ptr], integer)
            get_property = bind('XGetWindowProperty', [ptr, ul, ul, C.c_long, C.c_long,
                integer, ul, C.POINTER(ul), C.POINTER(integer), C.POINTER(ul),
                C.POINTER(ul), C.POINTER(ptr)], integer)
            get_geometry = bind('XGetGeometry', [ptr, ul, C.POINTER(ul), C.POINTER(integer),
                C.POINTER(integer), C.POINTER(C.c_uint), C.POINTER(C.c_uint),
                C.POINTER(C.c_uint), C.POINTER(C.c_uint)], integer)
            get_image = bind('XGetImage', [ptr, ul, integer, integer, C.c_uint,
                C.c_uint, ul, integer], ptr)
            pixel = bind('XGetPixel', [ptr, integer, integer], ul)
            destroy_image = bind('XDestroyImage', [ptr], integer)
            send_event = bind('XSendEvent', [ptr, ul, integer, C.c_long, ptr], integer)
            query_extension = bind('XQueryExtension', [ptr, C.c_char_p,
                C.POINTER(integer), C.POINTER(integer), C.POINTER(integer)], integer)
            class ButtonEvent(C.Structure):
                _fields_ = [('type', integer), ('serial', ul), ('send_event', integer),
                    ('display', ptr), ('window', ul), ('root', ul), ('subwindow', ul),
                    ('time', ul), ('x', integer), ('y', integer), ('x_root', integer),
                    ('y_root', integer), ('state', C.c_uint), ('button', C.c_uint),
                    ('same_screen', integer)]
            class Event(C.Union):
                _fields_ = [('button', ButtonEvent), ('padding', C.c_long * 24)]
            display = open_display(env['DISPLAY'].encode())
            assert display
            opcode, first_event, first_error = integer(), integer(), integer()
            randr = query_extension(display, b'RANDR', C.byref(opcode),
                C.byref(first_event), C.byref(first_error))
            assert bool(randr) == (mode == 'default'), 'explicit monitor backend unavailable'
            if mode == 'xinerama':
                assert query_extension(display, b'XINERAMA', C.byref(opcode),
                    C.byref(first_event), C.byref(first_error)), 'Xinerama mandatory'
            def property_value(win, name, expected_format):
                actual, fmt, count, after, data = ul(), integer(), ul(), ul(), ptr()
                assert get_property(display, win, intern(display, name.encode(), 0), 0,
                    128, 0, 0, C.byref(actual), C.byref(fmt), C.byref(count),
                    C.byref(after), C.byref(data)) == 0
                try:
                    if fmt.value == 0 and count.value == 0:
                        return None
                    assert fmt.value == expected_format and after.value == 0 and data
                    if fmt.value == 8:
                        return C.string_at(data, count.value)
                    assert fmt.value == 32
                    # Xlib exposes format32 slots in host-long storage; compare
                    # the protocol's actual low32 bits, not host sign extension.
                    return [v & 0xffffffff for v in C.cast(data, C.POINTER(ul))[:count.value]]
                finally:
                    if data:
                        free(data)
            def children():
                r, parent, ids, count = ul(), ul(), C.POINTER(ul)(), C.c_uint()
                assert query_tree(display, root(display), C.byref(r), C.byref(parent),
                    C.byref(ids), C.byref(count))
                try:
                    return list(ids[:count.value])
                finally:
                    if ids:
                        free(ids)
            def wait_for(predicate, message):
                end = time.monotonic() + 10
                while True:
                    assert server.poll() is None, 'private Xvfb exited'
                    assert child is None or child.poll() is None, message
                    sync(display, 0)
                    result = predicate()
                    if result:
                        return result
                    assert time.monotonic() < end, message
                    time.sleep(0.02)
            def color(win, x, y):
                image = get_image(display, win, x, y, 1, 1, ul(-1).value, 2)
                assert image
                try:
                    return pixel(image, 0, 0) & 0xffffff
                finally:
                    destroy_image(image)
            helped = subprocess.run([binary, '-h'], env=env, capture_output=True, timeout=10)
            assert helped.returncode == 0 and helped.stderr == b''
            assert helped.stdout.startswith(b'lemonbar version 1.4\nusage: ')
            assert b'\t-p Don\'t close after the data ends\n' in helped.stdout
            assert b'\t-o Add randr output by name\n' in helped.stdout
            bad = subprocess.run([binary, '-g', '999x999+0+0'], env=env,
                input=b'', capture_output=True, timeout=10)
            assert (bad.returncode, bad.stdout, bad.stderr) == (1, b'',
                b"The geometry specified doesn't fit the screen!\n")
            marker = chr(37)
            for permanent in (False, True):
                old = set(children())
                name = 'lemonbar-private-' + str(int(permanent))
                args = [binary, '-g', '160x24+7+9', '-n', name, '-f', 'fixed',
                    '-B', '#112233', '-F', '#ffffff', '-U', '#ee1100', '-u', '2']
                if permanent:
                    args += ['-p', '-b', '-d']
                child = subprocess.Popen(args, env=env, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                win = wait_for(lambda: next(iter(set(children()) - old), 0), 'bar window absent')
                wait_for(lambda: property_value(win, 'WM_NAME', 8) == name.encode(), 'WM_NAME absent')
                assert property_value(win, 'WM_CLASS', 8) == b'lemonbar\0Bar'
                assert property_value(win, '_NET_WM_WINDOW_TYPE', 32) == [
                    intern(display, b'_NET_WM_WINDOW_TYPE_DOCK', 0)]
                assert property_value(win, '_NET_WM_DESKTOP', 32) == [0xffffffff]
                r, x, y, w, h, border, depth = ul(), integer(), integer(), C.c_uint(), C.c_uint(), C.c_uint(), C.c_uint()
                assert get_geometry(display, win, C.byref(r), C.byref(x), C.byref(y),
                    C.byref(w), C.byref(h), C.byref(border), C.byref(depth))
                assert (x.value, y.value, w.value, h.value) == (7, 207 if permanent else 9, 160, 24)
                expected = [0] * 12
                if permanent:
                    expected[3], expected[10], expected[11] = 24, 7, 166
                else:
                    expected[2], expected[8], expected[9] = 24, 7, 166
                assert property_value(win, '_NET_WM_STRUT_PARTIAL', 32) == expected
                # A complete input line changes independently observed X pixels;
                # the clickable offset uses no font-dependent width assumptions.
                line = marker + '{B#335577}' + marker + '{+u}' + marker + '{A:private-click:}'
                line += marker + '{O60}' + marker + '{A}' + marker + '{-u}UTF-8: é ' + marker + marker + '\n'
                child.stdin.write(line.encode())
                child.stdin.flush()
                wait_for(lambda: color(win, 5, 5) == 0x335577 and color(win, 5, 23) == 0xee1100,
                    'format/offset/underline pixels absent')
                event = Event()
                event.button = ButtonEvent(4, 0, 1, display, win, root(display), 0,
                    0, 5, 5, 12, y.value + 5, 0, 1, 1)
                assert send_event(display, win, 0, 1 << 2, C.byref(event))
                sync(display, 0)
                assert select.select([child.stdout], [], [], 10)[0], 'click output absent'
                assert os.read(child.stdout.fileno(), 128) == b'private-click\n'
                child.stdin.close()
                child.stdin = None
                if permanent:
                    # EOF intentionally leaves -p alive. Send a real second
                    # click after EOF to prove the event loop still responds.
                    assert send_event(display, win, 0, 1 << 2, C.byref(event))
                    sync(display, 0)
                    assert select.select([child.stdout], [], [], 10)[0]
                    assert os.read(child.stdout.fileno(), 128) == b'private-click\n'
                    child.terminate()
                out, err = child.communicate(timeout=10)
                assert (child.returncode, out, err) == (0, b'', b''), (child.returncode, out, err)
                child = None
                sync(display, 0)
                assert win not in children(), 'bar cleanup did not destroy its window'
        finally:
            if child is not None:
                if child.poll() is None:
                    child.kill()
                child.communicate(timeout=5)
            if display:
                close_display(display)
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
LEMONBAR_QA
cat > downstream-smoke.sh <<'LEMONBAR_SMOKE'
#!/bin/bash
set -euo pipefail
test -x /usr/bin/lemonbar
test -f /usr/share/licenses/lemonbar/LICENSE
test -f /usr/share/licenses/lemonbar-tests/LICENSE
test -f /usr/share/doc/lemonbar/README.pod
python3 -I -B /usr/libexec/lemonbar/qa.py /usr/bin/lemonbar
LEMONBAR_SMOKE

%build
# Environment flags let original += retain all original compiler/linker defaults.
export CFLAGS='%{optflags}'
export LDFLAGS='%{?build_ldflags}'
%make_build CC=gcc
# Also preserve the upstream CI's supplementary Xinerama configuration, isolated
# from the default binary that is installed. No original test is removed.
mkdir downstream-xinerama
cp -p Makefile lemonbar.c utils.c utils.h downstream-xinerama/
( cd downstream-xinerama; CFLAGS="$CFLAGS -DWITH_XINERAMA=1" %make_build CC=gcc )

%install
# Original install also generates the manpage through original doc/pod2man.
%make_install PREFIX=%{_prefix}
install -Dpm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/lemonbar/qa.py
install -Dpm 0755 downstream-smoke.sh %{buildroot}%{_libexecdir}/lemonbar/smoke.sh

%check
python3 -I -B downstream-qa.py ./lemonbar
python3 -I -B downstream-qa.py ./downstream-xinerama/lemonbar xinerama
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/lemonbar

%files
%license LICENSE
%doc README.pod
%{_bindir}/lemonbar
%{_mandir}/man1/lemonbar.1*

%files tests
%license LICENSE
%{_libexecdir}/lemonbar

%changelog
* Tue Oct 20 2026 openEuler RISC-V Packaging <noreply@example.invalid> - 1.5-1
- Preserve defaults and internal version, test both monitor build configurations.
