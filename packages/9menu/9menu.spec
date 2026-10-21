# SPDX-License-Identifier: Apache-2.0
Name:           9menu
Version:        1.11
Release:        2%{?dist}
Summary:        Small X menu for executing shell commands
License:        LicenseRef-9menu
URL:            https://github.com/arnoldrobbins/9menu
# Official fixed source URL is recorded in sources.yaml; original notice is README.
Source0:        9menu-1.11.tar.gz
BuildRequires:  gcc make imake cpp libX11-devel xorg-x11-proto-devel
BuildRequires:  coreutils diffutils python3 bash xorg-x11-server-Xvfb xorg-x11-fonts
Requires:       libX11

%description
9menu creates a simple X menu whose selections execute shell commands.
The exact custom upstream license and its notice-preservation and modified-
functionality conditions are retained in the installed README license notice.

%package tests
Summary:        Mandatory private-X-server semantic tests for 9menu
Requires:       %{name} = %{version}-%{release}
Requires:       python3 bash libX11 xorg-x11-server-Xvfb xorg-x11-fonts

%description tests
Mandatory bounded, owned-X-server tests for the packaged 9menu executable.

%prep
%setup -q -n 9menu-baa949d59ff875b8f9863e26c7b422b6985edff6
# Original Imake rules consume .man, but the release supplies the same .1 text.
# Alias exact bytes only; preserve the original default CppManTarget processing.
cp -p 9menu.1 9menu.man
cmp 9menu.1 9menu.man
cat > downstream-qa.py <<'NINEMENU_QA'
"""Mandatory target-only 9menu semantics on an owned private X server."""
import ctypes as C
import ctypes.util
import os
from pathlib import Path
import select
import shlex
import signal
import subprocess
import sys
import tempfile
import time

binary = str(Path(sys.argv[1]).resolve(strict=True))
env = dict(os.environ, LC_ALL='C')
for args in (['-version'], ['-label', '9menu-empty'], ['-unknown']):
    result = subprocess.run([binary] + args, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=env, timeout=10, check=False)
    assert result.returncode == 0
    if args == ['-version']:
        assert result.stdout == b'9menu version 1.11\n' and result.stderr == b''
    else:
        assert result.stdout == b'' and result.stderr.startswith(b'usage: 9menu ')
        assert result.stderr.endswith(b'[-warp] [-version] menitem:command ...\n')
result = subprocess.run([binary, '-display', 'definitely-invalid', 'exit'],
                        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE, env=env, timeout=10, check=False)
assert result.returncode == 1 and result.stdout == b''
assert result.stderr == b'9menu: cannot open display definitely-invalid\n'

U = C.c_ulong
D = C.c_void_p
class Attributes(C.Structure):
    _fields_ = [(n, C.c_int) for n in ('x', 'y', 'width', 'height', 'border_width', 'depth')] + [
        ('visual', D), ('root', U), ('c_class', C.c_int), ('bit_gravity', C.c_int),
        ('win_gravity', C.c_int), ('backing_store', C.c_int), ('backing_planes', U),
        ('backing_pixel', U), ('save_under', C.c_int), ('colormap', U),
        ('map_installed', C.c_int), ('map_state', C.c_int), ('all_event_masks', C.c_long),
        ('your_event_mask', C.c_long), ('do_not_propagate_mask', C.c_long),
        ('override_redirect', C.c_int), ('screen', D)]
class Button(C.Structure):
    _fields_ = [('type', C.c_int), ('serial', U), ('send_event', C.c_int),
        ('display', D), ('window', U), ('root', U), ('subwindow', U), ('time', U),
        ('x', C.c_int), ('y', C.c_int), ('x_root', C.c_int), ('y_root', C.c_int),
        ('state', C.c_uint), ('button', C.c_uint), ('same_screen', C.c_int)]
class Key(C.Structure):
    _fields_ = Button._fields_[:-2] + [('keycode', C.c_uint), ('same_screen', C.c_int)]
class MessageData(C.Union):
    _fields_ = [('b', C.c_char * 20), ('s', C.c_short * 10), ('l', C.c_long * 5)]
class Message(C.Structure):
    _fields_ = [('type', C.c_int), ('serial', U), ('send_event', C.c_int),
        ('display', D), ('window', U), ('message_type', U), ('format', C.c_int),
        ('data', MessageData)]
class Event(C.Union):
    _fields_ = [('button', Button), ('key', Key), ('message', Message), ('pad', C.c_long * 24)]

x = C.CDLL(ctypes.util.find_library('X11'))
def signature(name, restype, *argtypes):
    function = getattr(x, name)
    function.restype, function.argtypes = restype, list(argtypes)
    return function
signature('XOpenDisplay', D, C.c_char_p)
signature('XDefaultRootWindow', U, D)
signature('XQueryTree', C.c_int, D, U, C.POINTER(U), C.POINTER(U), C.POINTER(C.POINTER(U)), C.POINTER(C.c_uint))
signature('XFetchName', C.c_int, D, U, C.POINTER(C.c_void_p))
signature('XFree', C.c_int, D)
signature('XGetWindowAttributes', C.c_int, D, U, C.POINTER(Attributes))
signature('XSendEvent', C.c_int, D, U, C.c_int, C.c_long, C.POINTER(Event))
signature('XKeysymToKeycode', C.c_ubyte, D, U)
signature('XInternAtom', U, D, C.c_char_p, C.c_int)
signature('XSync', C.c_int, D, C.c_int)
signature('XCloseDisplay', C.c_int, D)

def stop(process):
    if process is None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    if process.poll() is None:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)

server = None
display = None
processes = []
with tempfile.TemporaryDirectory(prefix='9menu-qa-') as temp:
    directory = Path(temp)
    read_fd, write_fd = os.pipe()
    try:
        with (directory / 'xvfb.log').open('wb') as log:
            server = subprocess.Popen(['/usr/bin/Xvfb', '-displayfd', str(write_fd),
                '-screen', '0', '640x480x24', '-nolisten', 'tcp',
                '-fp', '/usr/share/X11/fonts/misc'], stdout=log, stderr=log,
                pass_fds=(write_fd,), start_new_session=True)
        os.close(write_fd)
        write_fd = -1
        ready, _, _ = select.select([read_fd], [], [], 15)
        assert ready, ('mandatory private Xvfb failed', (directory / 'xvfb.log').read_bytes())
        number = os.read(read_fd, 64).strip()
        assert number.isdigit() and server.poll() is None
        display_name = b':' + number
        env['DISPLAY'] = display_name.decode()
        display = x.XOpenDisplay(display_name)
        assert display, (directory / 'xvfb.log').read_bytes()
        root = x.XDefaultRootWindow(display)
        protocols = x.XInternAtom(display, b'WM_PROTOCOLS', 0)
        delete = x.XInternAtom(display, b'WM_DELETE_WINDOW', 0)
        assert protocols and delete

        def wait(predicate, process, description):
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                answer = predicate()
                if answer:
                    return answer
                assert process.poll() is None, (description, process.returncode)
                assert server.poll() is None
                time.sleep(0.02)
            raise AssertionError(('timeout', description, (directory / 'xvfb.log').read_bytes()))

        def find_window(label):
            root_return, parent = U(), U()
            children, count = C.POINTER(U)(), C.c_uint()
            assert x.XQueryTree(display, root, C.byref(root_return), C.byref(parent), C.byref(children), C.byref(count))
            found = None
            try:
                for i in range(count.value):
                    name = C.c_void_p()
                    if x.XFetchName(display, children[i], C.byref(name)) and name.value:
                        try:
                            if C.string_at(name) == label.encode():
                                attributes = Attributes()
                                assert x.XGetWindowAttributes(display, children[i], C.byref(attributes))
                                if attributes.map_state == 2:
                                    assert attributes.width > 0 and attributes.height > 0
                                    found = (int(children[i]), attributes)
                        finally:
                            x.XFree(name)
            finally:
                if children:
                    x.XFree(C.cast(children, D))
            return found

        def launch(label, items, options=(), input_data=None):
            process = subprocess.Popen([binary, '-label', label] + list(options) + items,
                stdin=subprocess.PIPE if input_data is not None else subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=env,
                start_new_session=True)
            processes.append(process)
            if input_data is not None:
                process.stdin.write(input_data)
                process.stdin.close()
            window, attributes = wait(lambda: find_window(label), process, 'map/default-font window ' + label)
            return process, window, attributes

        def button(window, attributes, row, count, number=1):
            assert attributes.height == count * (attributes.height // count) and 0 <= row < count
            event = Event()
            event.button.type, event.button.display = 5, display
            event.button.window, event.button.root = window, root
            event.button.x = min(2, attributes.width - 1)
            event.button.y = row * (attributes.height // count) + attributes.height // count // 2
            event.button.button, event.button.same_screen = number, 1
            assert x.XSendEvent(display, window, 0, 1 << 3, C.byref(event))
            x.XSync(display, 0)

        def key(window, keysym):
            event = Event()
            event.key.type, event.key.display = 2, display
            event.key.window, event.key.root = window, root
            event.key.keycode = x.XKeysymToKeycode(display, keysym)
            event.key.same_screen = 1
            assert event.key.keycode and x.XSendEvent(display, window, 0, 1, C.byref(event))
            x.XSync(display, 0)

        def close_window(process, window):
            event = Event()
            event.message.type, event.message.display = 33, display
            event.message.window, event.message.message_type = window, protocols
            event.message.format, event.message.data.l[0] = 32, delete
            assert x.XSendEvent(display, window, 0, 0, C.byref(event))
            x.XSync(display, 0)
            assert process.wait(timeout=15) == 0
            assert process.stderr.read() == b''

        first, second = directory / 'first', directory / 'second'
        command_a = 'printf A > ' + shlex.quote(str(first))
        command_b = 'printf B > ' + shlex.quote(str(second))
        process, window, attributes = launch('9menu-distinct', ['alpha:' + command_a, 'beta:' + command_b, 'exit'])
        button(window, attributes, 0, 3, 2)
        key(window, 0xff54)  # Down from original mapped first row to second.
        key(window, 0xff0d)  # Return must execute beta, not alpha.
        wait(lambda: second.exists() and second.read_bytes() == b'B', process, 'keyboard distinct command')
        assert second.read_bytes() == b'B' and not first.exists()
        button(window, attributes, 0, 3)
        wait(lambda: first.exists() and first.read_bytes() == b'A', process, 'left mouse distinct command')
        assert first.read_bytes() == b'A' and second.read_bytes() == b'B'
        close_window(process, window)

        process, window, attributes = launch('9menu-popup', ['wrong:exit 12', 'wanted:exit 37'], ['-popup', '-shell', '/nonexistent/9menu-shell'])
        button(window, attributes, 1, 2, 3)
        assert process.wait(timeout=15) == 37 and process.stderr.read() == b''

        marker = directory / 'file-command'
        menu = directory / 'menu.txt'
        menu.write_text('# ignored comment\n\\-dash:printf FILE > ' + shlex.quote(str(marker)) + '\nexit\n')
        process, window, attributes = launch('9menu-file', [], ['-file', str(menu)])
        button(window, attributes, 0, 2)
        wait(lambda: marker.exists() and marker.read_bytes() == b'FILE', process, 'file comment/escaped-label parsing')
        assert marker.read_bytes() == b'FILE'
        button(window, attributes, 1, 2, 3)
        assert process.wait(timeout=15) == 0 and process.stderr.read() == b''

        marker = directory / 'stdin-command'
        data = ('# stdin comment\n-label 9menu-stdin\nstdin:printf STDIN > ' + shlex.quote(str(marker)) + '\nexit\n').encode()
        process, window, attributes = launch('9menu-stdin', [], ['-file', '-'], data)
        button(window, attributes, 0, 2, 3)
        wait(lambda: marker.exists() and marker.read_bytes() == b'STDIN', process, 'stdin/options parsing and right-button command')
        assert marker.read_bytes() == b'STDIN'
        close_window(process, window)

        process, window, attributes = launch('9menu-exec', ['replace:exec exit 23'])
        button(window, attributes, 0, 1)
        assert process.wait(timeout=15) == 23 and process.stderr.read() == b''
    finally:
        for process in reversed(processes):
            stop(process)
        if display:
            x.XCloseDisplay(display)
        stop(server)
        os.close(read_fd)
        if write_fd >= 0:
            os.close(write_fd)
print('9menu private-Xvfb default-font/CLI/keyboard/mouse/file/stdin/popup/exec/WM_DELETE QA passed')
NINEMENU_QA

%build
# Regenerate from the original Imakefile for actual target architecture/configs.
# Do not reuse the shipped generated Linux2.2/i386 Makefile or disable defaults.
xmkmf
%make_build CC=gcc CDEBUGFLAGS='%{optflags}' LDOPTIONS='%{?build_ldflags}'

%install
# Keep original install and install.man; only standard RPM paths/modes override.
%make_install install.man BINDIR=%{_bindir} MANDIR=%{_mandir}/man1 MANSUFFIX=1 INSTPGMFLAGS='-m 0755'
install -D -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/9menu-tests/qa.py

%check
# No original test/check target exists; no upstream tests are deleted or skipped.
python3 downstream-qa.py ./9menu
python3 downstream-qa.py %{buildroot}%{_bindir}/9menu
cmp 9menu.1 9menu.man

%files
%license README
%doc ChangeLog 9menu.1
%{_bindir}/9menu
%{_mandir}/man1/9menu.1*

%files tests
%license README
%{_libexecdir}/9menu-tests/

%changelog
* Wed Oct 21 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11-2
- Wait for exact command marker bytes within existing bounded downstream QA waits.

* Tue Oct 20 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11-1
- Package official fixed 1.11 source with original custom notice and mandatory X QA.
