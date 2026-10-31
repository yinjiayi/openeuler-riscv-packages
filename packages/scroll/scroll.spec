# SPDX-License-Identifier: ISC
Name:           scroll
Version:        0.1
Release:        1%{?dist}
Summary:        Experimental terminal scrollback wrapper using a private PTY
License:        ISC
URL:            https://tools.suckless.org/scroll/
Source0:        https://dl.suckless.org/tools/scroll-0.1.tar.gz
# Exact original LICENSE from official 0.1 tag, omitted by its dist recipe.
Patch0:         0001-restore-official-release-license.patch
BuildRequires:  gcc
BuildRequires:  patch
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  bash
BuildRequires:  python3
ExclusiveArch:  riscv64

%description
Scroll is an experimental scrollback wrapper for terminals such as st. It keeps
child output in memory and handles default Shift-PageUp and Shift-PageDown keys.
Upstream explicitly does not recommend productive use. It is not a complete
terminal emulator and does not support arbitrary editing of historical lines.

%package tests
Summary:        Mandatory private-PTY semantic checks for scroll
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash
BuildArch:      noarch

%description tests
Private-PTY history, key forwarding, alternate-screen, resize, child-exit and
terminal-restoration checks. Upstream's complete original make test also remains
mandatory during the build, including its unmodified byte-exact up.log fixture.

%prep
%autosetup -n scroll-0.1 -p1
# Package-local notice is an exact upstream LICENSE, not a relicensing assertion.
echo '52f5f340941b3f63fc16882f3e17a9aa28751f7aedaf90f88922d14654b00e62  LICENSE' | sha256sum -c -
cat > downstream-upstream-tests.py <<'SCROLL_UPSTREAM'
"""Target-only complete original make-test driver with held-open parent input."""
import os
import signal
import subprocess
import sys

assert sys.argv[1:3] == ['make', 'test']
process = subprocess.Popen(sys.argv[1:], stdin=subprocess.PIPE,
                           start_new_session=True, close_fds=True)
try:
    # Do not communicate(): it would close stdin and make original ptty close its
    # private master before its child finishes. Keep this writer open while wait
    # observes original make test, including unmodified up.sh's own pipeline.
    status = process.wait(timeout=60)
except BaseException:
    if process.poll() is None:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
    raise
finally:
    process.stdin.close()
raise SystemExit(status)
SCROLL_UPSTREAM
cat > downstream-qa.py <<'SCROLL_QA'
"""Mandatory target-only private-PTY checks; never executed on the intake host."""
import errno
import fcntl
import os
from pathlib import Path
import select
import signal
import struct
import subprocess
import sys
import termios
import time

binary = str(Path(sys.argv[1]).resolve(strict=True))
env = dict(os.environ, LC_ALL='C', TERM='xterm', POSIXLY_CORRECT='1')
for args, expected in ((['-v'], binary + ' 0.1\n'),
                       (['-h'], 'usage: ' + binary + ' [-Mvh] [-m mem] [program]\n'),
                       ([], 'parent it not a tty\n')):
    result = subprocess.run([binary] + args, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=env, timeout=10, check=False)
    assert result.returncode == 1 and result.stdout == b''
    assert result.stderr == expected.encode(), (args, result.stderr)

fixture = r'''
import fcntl, os, signal, struct, sys, termios, tty
tty.setraw(0)
def output(data):
    os.write(1, data)
def resized(signum, frame):
    assert signum == signal.SIGWINCH
    rows, cols, _, _ = struct.unpack('HHHH', fcntl.ioctl(0, termios.TIOCGWINSZ, b'\0' * 8))
    output(('SIZE:' + str(rows) + ':' + str(cols) + '\r\n').encode())
signal.signal(signal.SIGWINCH, resized)
output(('PID:' + str(os.getpid()) + '\r\n').encode())
for number in range(1, 50):
    output((str(number) + '\r\n').encode())
output(b'READY')
while True:
    key = os.read(0, 1)
    if key == b'x':
        output(b'INPUT:78\r\n')
    elif key == b'a':
        output(b'\x1b[?1049hALT-READY')
        packet = b''
        while len(packet) < 6:
            chunk = os.read(0, 6 - len(packet))
            assert chunk
            packet += chunk
        output(b'ALTKEY:' + packet.hex().encode() + b'\r\n')
    elif key == b'n':
        output(b'\x1b[?1049lBACK\r\n')
    elif key == b'q':
        sys.exit(37)
    else:
        raise AssertionError(('unexpected input', key))
'''

master, slave = os.openpty()
fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 25, 80, 0, 0))
original = termios.tcgetattr(slave)
process = None
child_pid = None
wire = bytearray()
answered = 0

def pump(deadline):
    global answered
    remaining = deadline - time.monotonic()
    assert remaining > 0, ('PTY timeout', bytes(wire[-1000:]))
    ready, _, _ = select.select([master], [], [], min(remaining, 0.2))
    if not ready:
        assert process.poll() is None, ('early wrapper exit', process.returncode, bytes(wire))
        return
    try:
        chunk = os.read(master, 65536)
    except OSError as error:
        if error.errno == errno.EIO:
            raise AssertionError(('unexpected PTY EOF', process.poll(), bytes(wire))) from error
        raise
    assert chunk
    wire.extend(chunk)
    queries = wire.count(b'\x1b[6n')
    while answered < queries:
        os.write(master, b'\x1b[25;1R')
        answered += 1

def until(token, offset=0):
    deadline = time.monotonic() + 15
    while token not in wire[offset:]:
        pump(deadline)
    return bytes(wire[offset:])

def send(data):
    offset = len(wire)
    assert os.write(master, data) == len(data)
    return offset

try:
    process = subprocess.Popen([binary, sys.executable, '-I', '-B', '-u', '-c', fixture],
                               stdin=slave, stdout=slave, stderr=slave, env=env,
                               start_new_session=True, close_fds=True)
    first = until(b'READY')
    line = first.split(b'PID:', 1)[1].split(b'\r\n', 1)[0]
    assert line.isdigit()
    child_pid = int(line)
    assert child_pid > 1 and child_pid != process.pid
    assert b'1\r\n2\r\n' in first and b'48\r\n49\r\nREADY' in first
    offset = send(b'\x1b[5;2~')
    up = until(b'\x1b[25;0H', offset)
    expected = (b'\x1b[6n\x1b[25T\x1b[0;0H\x1b[?25l\r\n' +
                b'\r\n'.join(str(i).encode() for i in range(1, 26)) +
                b'\x1b[25;0H')
    assert up == expected, ('exact original 25-line history semantics', up, expected)
    offset = send(b'\x1b[6;2~')
    down = until(b'READY', offset)
    assert b'\x1b[?25h' in down and b'49\x1b[?25h\r\nREADY' in down and b'\x1b[6n' not in down, ('exact original latest-line/cursor/prompt semantics', down)
    offset = send(b'x')
    assert b'INPUT:78\r\n' in until(b'INPUT:78\r\n', offset)
    offset = send(b'a')
    until(b'ALT-READY', offset)
    offset = send(b'\x1b[5;2~')
    alternate = until(b'ALTKEY:1b5b353b327e\r\n', offset)
    assert b'\x1b[6n' not in alternate and b'\x1b[25T' not in alternate
    offset = send(b'n')
    until(b'BACK\r\n', offset)
    offset = len(wire)
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 30, 90, 0, 0))
    os.kill(process.pid, signal.SIGWINCH)
    until(b'SIZE:30:90\r\n', offset)
    until(b'\x1b[?25h', offset)
    send(b'q')
    assert process.wait(timeout=15) == 37
    assert termios.tcgetattr(slave) == original, 'wrapper did not restore private terminal'
finally:
    for group in (child_pid, process.pid if process is not None else None):
        if group is not None:
            try:
                os.killpg(group, signal.SIGKILL)
            except ProcessLookupError:
                pass
    if process is not None:
        process.wait(timeout=5)
    os.close(master)
    os.close(slave)
print('scroll private-PTY CLI/history/input/alternate-screen/resize/exit/restoration QA passed')
SCROLL_QA

%build
# Keep upstream -Os, VERSION/DEFAULT_SOURCE CPPFLAGS, default all and -lutil.
# Defer standalone -s stripping to normal RPM processing for debug products.
%make_build CC=gcc CFLAGS='%{optflags} -Os' LDFLAGS='%{?build_ldflags}'

%install
%make_install PREFIX=%{_prefix} BINDIR=%{_bindir} MANDIR=%{_mandir}
install -Dpm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/scroll-tests/qa.py

%check
# Keep parent input open through original ptty checks; bounded whole original target.
python3 -I -B downstream-upstream-tests.py make test CC=gcc CFLAGS='%{optflags} -Os' LDFLAGS='%{?build_ldflags}'
python3 -I -B downstream-qa.py ./scroll
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/scroll

%files
%license LICENSE
%doc README TODO
%{_bindir}/scroll
%{_mandir}/man1/scroll.1*

%files tests
%license LICENSE
%{_libexecdir}/scroll-tests

%changelog
* Tue Oct 20 2026 openEuler RISC-V Packaging <noreply@example.invalid> - 0.1-1
- Preserve original tests/default bindings, recover omitted original ISC notice.
- Add mandatory private-PTY built, staged and installed semantic checks.
