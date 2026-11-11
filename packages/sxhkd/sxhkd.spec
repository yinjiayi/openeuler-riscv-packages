# SPDX-License-Identifier: BSD-2-Clause
Name:           sxhkd
Version:        0.6.3
Release:        1%{?dist}
Summary:        Simple X hotkey daemon with keyboard and mouse chord bindings
License:        BSD-2-Clause
URL:            https://github.com/baskerville/sxhkd
Source0:        https://codeload.github.com/baskerville/sxhkd/tar.gz/2cc7aca40f38cd47fbeea1f37fe310ef34386435#/sxhkd-0.6.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  python3
BuildRequires:  libX11
BuildRequires:  libXtst
BuildRequires:  xorg-x11-server-Xvfb
ExclusiveArch:  riscv64

%description
Sxhkd is an X hotkey daemon that executes shell commands for configured keyboard
and mouse chords, brace expansions and chained key sequences. Original default
build and installation semantics are preserved without source patches.

%package tests
Summary:        Offline semantic checks for sxhkd
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       libX11
Requires:       libXtst
Requires:       xorg-x11-server-Xvfb
Requires:       bash
BuildArch:      noarch

%description tests
Mandatory isolated Xvfb and real XTEST input checks of keyboard/button bindings,
release/control/brace/chain behavior, configuration, signals and child commands.
Upstream has no original test target; no test is disabled or replaced.

%prep
%autosetup -n sxhkd-2cc7aca40f38cd47fbeea1f37fe310ef34386435
cat > downstream-qa.py <<'SXHKD_QA'
#!/usr/bin/python3
"""Mandatory target-only real-event workload; never run on the intake host."""
import ctypes as C
import os
from pathlib import Path
import select
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time


def main():
    binary = str(Path(sys.argv[1]).resolve(strict=True))
    env = dict(os.environ, LC_ALL='C', DISPLAY='invalid-display')
    for option, expected in [('-v', b'0.6.3\n'), ('-h',
            b'sxhkd [-h|-v|-m COUNT|-t TIMEOUT|-c CONFIG_FILE|-r REDIR_FILE|-s STATUS_FIFO|-a ABORT_KEYSYM] [EXTRA_CONFIG ...]\n')]:
        result = subprocess.run([binary, option], env=env, capture_output=True, timeout=10)
        assert (result.returncode, result.stdout, result.stderr) == (0, expected, b'')
    result = subprocess.run([binary], env=env, capture_output=True, timeout=10)
    assert (result.returncode, result.stdout, result.stderr) == (1, b'', b"Can't open display.\n")
    xvfb = shutil.which('Xvfb')
    assert xvfb, 'private Xvfb is mandatory, not optional'
    with tempfile.TemporaryDirectory(prefix='sxhkd-qa-') as temp:
        work = Path(temp)
        rd, wr = os.pipe()
        server = child = display = None
        fifo_fd = None
        held = set()
        try:
            with (work / 'xvfb.log').open('wb') as log:
                server = subprocess.Popen([xvfb, '-displayfd', str(wr), '-screen', '0',
                    '320x240x24', '-nolisten', 'tcp', '-noreset', '+extension', 'XTEST'],
                    pass_fds=(wr,), stdin=subprocess.DEVNULL, stdout=log, stderr=log)
            os.close(wr)
            wr = None
            deadline = time.monotonic() + 20
            token = b''
            while b'\n' not in token:
                assert server.poll() is None, (work / 'xvfb.log').read_bytes()
                remaining = deadline - time.monotonic()
                assert remaining > 0 and select.select([rd], [], [], remaining)[0]
                data = os.read(rd, 64)
                assert data
                token += data
                assert len(token) < 64
            assert token.endswith(b'\n') and token[:-1].isdigit()
            env.update(DISPLAY=':' + token[:-1].decode('ascii'), SXHKD_SHELL='/bin/sh',
                       SHELL='/not-the-selected-shell', XDG_CONFIG_HOME=str(work / 'config'))
            lib = C.CDLL('libX11.so.6')
            xtest = C.CDLL('libXtst.so.6')
            ptr, integer, ul = C.c_void_p, C.c_int, C.c_ulong
            def bind(library, name, arguments, result):
                fn = getattr(library, name)
                fn.argtypes, fn.restype = arguments, result
                return fn
            open_display = bind(lib, 'XOpenDisplay', [C.c_char_p], ptr)
            close_display = bind(lib, 'XCloseDisplay', [ptr], integer)
            root_window = bind(lib, 'XDefaultRootWindow', [ptr], ul)
            sync = bind(lib, 'XSync', [ptr, integer], integer)
            keysym = bind(lib, 'XStringToKeysym', [C.c_char_p], ul)
            keycode = bind(lib, 'XKeysymToKeycode', [ptr, ul], C.c_ubyte)
            grab = bind(lib, 'XGrabKey', [ptr, integer, C.c_uint, ul, integer, integer, integer], integer)
            ungrab = bind(lib, 'XUngrabKey', [ptr, integer, C.c_uint, ul], integer)
            query = bind(xtest, 'XTestQueryExtension', [ptr, C.POINTER(integer),
                C.POINTER(integer), C.POINTER(integer), C.POINTER(integer)], integer)
            fake_key = bind(xtest, 'XTestFakeKeyEvent', [ptr, C.c_uint, integer, ul], integer)
            fake_button = bind(xtest, 'XTestFakeButtonEvent', [ptr, C.c_uint, integer, ul], integer)
            fake_motion = bind(xtest, 'XTestFakeMotionEvent', [ptr, integer, integer, integer, ul], integer)
            display = open_display(env['DISPLAY'].encode())
            assert display
            values = [integer() for _ in range(4)]
            assert query(display, *(C.byref(v) for v in values)), 'real XTEST is mandatory'
            root = root_window(display)
            class XError(C.Structure):
                _fields_ = [('type', integer), ('display', ptr), ('resourceid', ul),
                    ('serial', ul), ('error_code', C.c_ubyte),
                    ('request_code', C.c_ubyte), ('minor_code', C.c_ubyte)]
            callback_type = C.CFUNCTYPE(integer, ptr, C.POINTER(XError))
            errors = []
            @callback_type
            def error_handler(_display, error):
                errors.append((error.contents.error_code, error.contents.request_code))
                return 0
            set_error = bind(lib, 'XSetErrorHandler', [callback_type], ptr)
            set_error(error_handler)
            def code(name):
                value = keycode(display, keysym(name.encode()))
                assert value, name
                return value
            def owned(name):
                # Only BadAccess from GrabKey means another client owns this key.
                # Successful diagnostic grabs are always undone before returning.
                sync(display, 0)
                assert not errors, errors
                grab(display, code(name), 0, root, 0, 1, 1)
                sync(display, 0)
                conflict = list(errors)
                errors.clear()
                assert conflict in ([], [(10, 33)]), conflict
                ungrab(display, code(name), 0, root)
                sync(display, 0)
                assert not errors, errors
                return bool(conflict)
            def wait_for(predicate, description):
                until = time.monotonic() + 15
                while not predicate():
                    assert server.poll() is None, (work / 'xvfb.log').read_bytes()
                    assert child is None or child.poll() is None, (work / 'daemon.log').read_bytes()
                    assert time.monotonic() < until, description
                    time.sleep(0.01)
            def key(name, pressed):
                value = code(name)
                assert fake_key(display, value, int(pressed), 0)
                if pressed:
                    held.add(value)
                else:
                    held.discard(value)
                sync(display, 0)
                assert not errors, errors
            def tap(name):
                key(name, True)
                key(name, False)
            default = work / 'config/sxhkd/sxhkdrc'
            default.parent.mkdir(parents=True)
            output = work / 'commands'
            status = work / 'status'
            os.mkfifo(status, 0o600)
            fifo_fd = os.open(status, os.O_RDWR | os.O_NONBLOCK)
            captured = bytearray()
            def drain():
                while select.select([fifo_fd], [], [], 0)[0]:
                    captured.extend(os.read(fifo_fd, 8192))
                return bytes(captured)
            def command(label):
                return ';echo ' + label + ':$SXHKD_PID'
            pairs = [('F1', command('press')), ('@F2', command('release')),
                ('ctrl + F3', command('control')), ('F{4,5}', command('brace-{one,two}')),
                ('F6; F7', command('chain')), ('button3', command('button')),
                ('F12', command('barrier'))]
            def write_config(path, bindings):
                path.write_text(''.join(hotkey + '\n\t' + action + '\n' for hotkey, action in bindings))
            write_config(default, pairs)
            extra = work / 'extra'
            write_config(extra, [('F8', command('extra'))])
            def launch(arguments):
                nonlocal child
                with (work / 'daemon.log').open('ab') as log:
                    child = subprocess.Popen([binary, '-r', str(output), '-s', str(status), *arguments],
                        env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
            def lines():
                return output.read_text().splitlines() if output.exists() else []
            def expect(label, before):
                wanted = label + ':' + str(child.pid)
                wait_for(lambda: len(lines()) > before, 'command did not run: ' + label)
                assert lines()[before:] == [wanted], lines()
                # This line is emitted after the synchronous child completes.
                wait_for(lambda: ('Cecho ' + label + ':$SXHKD_PID\n').encode() in drain(), 'missing command FIFO status')
            launch([str(extra)])
            wait_for(lambda: owned('F12') and owned('F8'), 'default and extra config grabs')
            for hotkey, label in [('F1', 'press'), ('F4', 'brace-one'), ('F5', 'brace-two'), ('F8', 'extra')]:
                before = len(lines())
                tap(hotkey)
                expect(label, before)
            before = len(lines())
            key('F2', True)
            tap('F12')
            expect('barrier', before)
            assert not any(line.startswith('release:') for line in lines())
            before = len(lines())
            key('F2', False)
            expect('release', before)
            before = len(lines())
            key('Control_L', True)
            tap('F3')
            key('Control_L', False)
            expect('control', before)
            before = len(lines())
            tap('F6')
            wait_for(lambda: b'BBegin chain\n' in drain(), 'chain did not begin')
            assert len(lines()) == before
            tap('F7')
            expect('chain', before)
            wait_for(lambda: b'EEnd chain\n' in drain(), 'chain did not end')
            before = len(lines())
            assert fake_motion(display, 0, 100, 100, 0)
            assert fake_button(display, 3, 1, 0) and fake_button(display, 3, 0, 0)
            sync(display, 0)
            expect('button', before)
            child.send_signal(signal.SIGUSR2)
            wait_for(lambda: not owned('F12'), 'SIGUSR2 did not ungrab')
            child.send_signal(signal.SIGUSR2)
            wait_for(lambda: owned('F12'), 'SIGUSR2 did not regrab')
            write_config(default, [('F11', command('reloaded')), ('F12', command('barrier'))])
            child.send_signal(signal.SIGUSR1)
            wait_for(lambda: owned('F11') and not owned('F1'), 'SIGUSR1 did not replace grabs')
            before = len(lines())
            tap('F11')
            expect('reloaded', before)
            child.terminate()
            assert child.wait(timeout=10) == 0
            child = None
            assert not owned('F12') and not owned('F11'), 'termination leaked grabs'
            explicit = work / 'explicit'
            write_config(explicit, [('F10', command('explicit'))])
            # Upstream -r intentionally opens without O_TRUNC. Use a new file for
            # the second process rather than assuming a truncation contract.
            output.unlink()
            launch(['-c', str(explicit)])
            wait_for(lambda: owned('F10'), 'explicit config not loaded')
            assert not owned('F12') and not owned('F11'), 'explicit config did not override XDG default'
            before = len(lines())
            tap('F10')
            expect('explicit', before)
            child.send_signal(signal.SIGINT)
            assert child.wait(timeout=10) == 0
            child = None
            assert not owned('F10')
            assert not errors, errors
            print('sxhkd: CLI, real key/button events, release, control, brace, chain, extra/explicit/default config, PID/shell/redirection, FIFO, reload/toggle and cleanup passed')
        finally:
            if display:
                for value in held:
                    fake_key(display, value, 0, 0)
                sync(display, 0)
            if child is not None and child.poll() is None:
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait(timeout=5)
            if display:
                close_display(display)
            if fifo_fd is not None:
                os.close(fifo_fd)
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
SXHKD_QA

%build
# Environment flags retain every original appended compiler flag and CPPFLAGS.
export CFLAGS='%{optflags}'
export LDFLAGS='%{?build_ldflags}'
# Select upstream's original archive VERSION fallback, never a parent Git tag.
%make_build CC=gcc VERCMD=false

%install
# Original install ships the existing manpage and example directory unchanged.
%make_install PREFIX=%{_prefix} DOCPREFIX=%{_docdir}/sxhkd
install -Dpm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/sxhkd-tests/qa.py

%check
python3 -I -B downstream-qa.py ./sxhkd
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/sxhkd

%files
%license LICENSE
%doc README.md
%{_bindir}/sxhkd
%{_mandir}/man1/sxhkd.1*
%dir %{_docdir}/sxhkd
%{_docdir}/sxhkd/examples

%files tests
%license LICENSE
%{_libexecdir}/sxhkd-tests

%changelog
* Tue Oct 20 2026 openEuler RISC-V Packaging <noreply@example.invalid> - 0.6.3-1
- Preserve defaults and add mandatory private-display real-input semantic checks.
