# SPDX-License-Identifier: Apache-2.0
Name:           slstatus
Version:        1.1
Release:        1%{?dist}
Summary:        Small status monitor with default datetime output
License:        ISC
ExclusiveArch:  riscv64
URL:            https://tools.suckless.org/slstatus/
Source0:        slstatus-1.1.tar.gz
Patch0:         patches/0001-copy-interface-flags-before-free.patch
BuildRequires:  gcc make patch coreutils diffutils python3 bash
BuildRequires:  libX11-devel xorg-x11-proto-devel glibc-devel kernel-headers xorg-x11-server-Xvfb
Requires:       libX11

%description
slstatus supplies status to standard output or the root window WM_NAME.
The packaged original configuration displays date and time; optional hardware
and system metrics require upstream configuration and are not runtime-validated.

%package tests
BuildArch:      noarch
Summary:        Mandatory default-configuration semantic tests for slstatus
Requires:       %{name} = %{version}-%{release}
Requires:       python3 bash libX11 xorg-x11-server-Xvfb

%description tests
Bounded mandatory default datetime and owned private-X-server tests.

%prep
%autosetup -N -n slstatus-%{version}
# Retain exact prepatch source solely for deterministic regression negative control.
cp -p components/ip.c components/downstream-ip-original.c
echo 'db4673b802f09a7b9adf1a44e8d153200b91034a118b29430fc5cf94f5194e67  components/downstream-ip-original.c' | sha256sum -c -
%autopatch -p1
cat > downstream-qa.py <<'SLSTATUS_QA'
"""Mandatory target-only tests for the unchanged default datetime configuration.

These are functional checks, not native hardware, metric or timing benchmarks.
"""
import ctypes as C
from datetime import datetime, timezone
import os
from pathlib import Path
import re
import select
import signal
import subprocess
import sys
import tempfile
import time

binary = str(Path(sys.argv[1]).resolve(strict=True))
env = dict(os.environ, LC_ALL='C', TZ='UTC0', DISPLAY='slstatus-invalid-display')

def run(args, **kwargs):
    return subprocess.run([binary] + args, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env, timeout=15, check=False, **kwargs)

result = run(['-v'])
assert (result.returncode, result.stdout, result.stderr) == (1, b'', b'slstatus-1.1\n')
for args in (['-z'], ['unexpected'], ['-1', 'unexpected']):
    result = run(args)
    assert (result.returncode, result.stdout, result.stderr) == (
        1, b'', ('usage: ' + binary + ' [-v] [-s] [-1]\n').encode())
result = run([])
assert (result.returncode, result.stdout, result.stderr) == (
    1, b'', b'XOpenDisplay: Failed to open display\n')

def timestamp(data, earliest, latest):
    assert re.fullmatch(rb'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', data), repr(data)
    parsed = int(datetime.strptime(data.decode('ascii'), '%%Y-%%m-%%d %%H:%%M:%%S').replace(
        tzinfo=timezone.utc).timestamp())
    assert earliest <= parsed <= latest, (data, earliest, parsed, latest)
    return parsed

# -1 implies stdout, so no X server is available or required in this case.
for args in (['-1'], ['-s1'], ['--', '-1']):
    if args == ['--', '-1']:
        result = run(args)
        assert result.returncode == 1 and result.stdout == b''
        assert result.stderr == ('usage: ' + binary + ' [-v] [-s] [-1]\n').encode()
        continue
    before = int(time.time())
    result = run(args)
    after = int(time.time())
    assert result.returncode == 0 and result.stderr == b''
    assert result.stdout.endswith(b'\n') and result.stdout.count(b'\n') == 1
    timestamp(result.stdout[:-1], before, after)

with open('/dev/full', 'wb', buffering=0) as full:
    result = subprocess.run([binary, '-1'], stdin=subprocess.DEVNULL, stdout=full,
                            stderr=subprocess.PIPE, env=env, timeout=15, check=False)
assert result.returncode == 1 and result.stderr == b'puts: No space left on device\n'

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

process = None
try:
    start = int(time.time())
    process = subprocess.Popen([binary, '-s'], stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, start_new_session=True)
    pending = b''
    def line():
        global pending
        deadline = time.monotonic() + 15
        while b'\n' not in pending:
            assert process.poll() is None, process.returncode
            remaining = deadline - time.monotonic()
            assert remaining > 0, 'bounded stdout refresh timeout'
            ready, _, _ = select.select([process.stdout], [], [], remaining)
            assert ready, 'bounded stdout refresh timeout'
            chunk = os.read(process.stdout.fileno(), 4096)
            assert chunk
            pending += chunk
        value, pending = pending.split(b'\n', 1)
        timestamp(value, start, int(time.time()))
        return value
    first = line()
    # Observe normal periodic output changing with the original one-second clock.
    deadline = time.monotonic() + 15
    while line() == first:
        assert time.monotonic() < deadline
    os.kill(process.pid, signal.SIGUSR1)
    line()
    assert process.poll() is None, 'USR1 must redraw rather than terminate'
    os.kill(process.pid, signal.SIGTERM)
    tail, errors = process.communicate(timeout=15)
    assert process.returncode == 0 and errors == b''
    assert not (pending + tail) or (pending + tail).endswith(b'\n')
    for value in (pending + tail).splitlines():
        timestamp(value, start, int(time.time()))
finally:
    stop(process)

x = C.CDLL('libX11.so.6')
def signature(name, restype, *argtypes):
    function = getattr(x, name)
    function.restype, function.argtypes = restype, list(argtypes)
    return function
D, U = C.c_void_p, C.c_ulong
signature('XOpenDisplay', D, C.c_char_p)
signature('XDefaultRootWindow', U, D)
signature('XFetchName', C.c_int, D, U, C.POINTER(D))
signature('XStoreName', C.c_int, D, U, C.c_char_p)
signature('XSync', C.c_int, D, C.c_int)
signature('XFree', C.c_int, D)
signature('XCloseDisplay', C.c_int, D)

server, display = None, None
processes = []
with tempfile.TemporaryDirectory(prefix='slstatus-qa-') as temp:
    directory = Path(temp)
    read_fd, write_fd = os.pipe()
    try:
        with (directory / 'xvfb.log').open('wb') as log:
            server = subprocess.Popen(['/usr/bin/Xvfb', '-displayfd', str(write_fd),
                '-screen', '0', '320x240x24', '-nolisten', 'tcp'],
                stdout=log, stderr=log, pass_fds=(write_fd,), start_new_session=True)
        os.close(write_fd)
        write_fd = -1
        ready, _, _ = select.select([read_fd], [], [], 15)
        assert ready, ('mandatory private Xvfb', (directory / 'xvfb.log').read_bytes())
        number = os.read(read_fd, 64).strip()
        assert number.isdigit() and server.poll() is None
        display_name = b':' + number
        display = x.XOpenDisplay(display_name)
        assert display, (directory / 'xvfb.log').read_bytes()
        root = x.XDefaultRootWindow(display)
        xenv = dict(env, DISPLAY=display_name.decode())
        def name():
            data = D()
            status = x.XFetchName(display, root, C.byref(data))
            try:
                return C.string_at(data) if status and data.value else b''
            finally:
                if data.value:
                    x.XFree(data)
        def wait_name(process, start):
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                assert process.poll() is None and server.poll() is None
                value = name()
                if re.fullmatch(rb'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', value):
                    timestamp(value, start, int(time.time()))
                    return value
                time.sleep(0.02)
            raise AssertionError(('bounded root-name timeout', name(),
                                  (directory / 'xvfb.log').read_bytes()))
        for ending in (signal.SIGTERM, signal.SIGINT):
            sentinel = b'slstatus-owned-server-sentinel'
            assert x.XStoreName(display, root, sentinel)
            x.XSync(display, 0)
            assert name() == sentinel
            start = int(time.time())
            process = subprocess.Popen([binary], stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=xenv,
                start_new_session=True)
            processes.append(process)
            wait_name(process, start)
            assert x.XStoreName(display, root, sentinel)
            x.XSync(display, 0)
            os.kill(process.pid, signal.SIGUSR1)
            wait_name(process, start)
            assert process.poll() is None
            os.kill(process.pid, ending)
            output, errors = process.communicate(timeout=15)
            assert (process.returncode, output, errors) == (0, b'', b'')
            assert name() == b'', 'normal signal termination must clear owned root WM_NAME'
    finally:
        for process in processes:
            stop(process)
        if display:
            x.XCloseDisplay(display)
        stop(server)
        os.close(read_fd)
        if write_fd >= 0:
            os.close(write_fd)
SLSTATUS_QA
cat > downstream-ip-regression.c <<'SLSTATUS_IP'
/* SPDX-License-Identifier: Apache-2.0
 * Target-only deterministic regression fixture for Slstatus 1.1 up().
 * No actual interface, allocation lifetime or native kernel claim is made.
 */
#include <assert.h>
#include <ifaddrs.h>
#include <net/if.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include "slstatus.h"

char buf[1024];
static struct ifaddrs fixture;
static struct sockaddr address;
static unsigned int initial_flags, after_release_flags, releases;

int downstream_getifaddrs(struct ifaddrs **out)
{
    memset(&fixture, 0, sizeof fixture);
    memset(&address, 0, sizeof address);
    address.sa_family = AF_INET;
    fixture.ifa_name = "downstream-test";
    fixture.ifa_addr = &address;
    fixture.ifa_flags = initial_flags;
    *out = &fixture;
    return 0;
}

void downstream_freeifaddrs(struct ifaddrs *value)
{
    assert(value == &fixture);
    /* A static fake stays valid but changes deterministically on release. */
    fixture.ifa_flags = after_release_flags;
    releases++;
}

const char *downstream_original_up(const char *);

int main(void)
{
    initial_flags = IFF_UP;
    after_release_flags = 0;
    assert(strcmp(up("downstream-test"), "up") == 0);
    assert(releases == 1);
    assert(strcmp(downstream_original_up("downstream-test"), "down") == 0);
    assert(releases == 2);
    initial_flags = 0;
    after_release_flags = IFF_UP;
    assert(strcmp(up("downstream-test"), "down") == 0);
    assert(releases == 3);
    assert(strcmp(downstream_original_up("downstream-test"), "up") == 0);
    assert(releases == 4);
    assert(up("missing-interface") == NULL);
    assert(releases == 5);
    puts("slstatus ip up lifetime regression: patched positive and original negative controls passed");
    return 0;
}
SLSTATUS_IP

%build
# Preserve all22 default objects, version defines, C99 warnings and libX11.
# Standard RPM flags replace upstream stripping only; config is generated unchanged.
%make_build CC=gcc X11INC=%{_includedir} X11LIB=%{_libdir} CFLAGS='%{optflags} -std=c99 -pedantic -Wall -Wextra -Wno-unused-parameter' LDFLAGS='%{?build_ldflags}'
cmp config.def.h config.h

%install
%make_install PREFIX=%{_prefix} MANPREFIX=%{_mandir}
install -D -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/slstatus-tests/qa.py

%check
# No original test/check target exists; none is removed, disabled or replaced.
cmp config.def.h config.h
gcc %{optflags} -std=c99 -D_DEFAULT_SOURCE -UNDEBUG -I. -Dgetifaddrs=downstream_getifaddrs -Dfreeifaddrs=downstream_freeifaddrs -c components/ip.c -o downstream-ip-fixed.o
gcc %{optflags} -std=c99 -D_DEFAULT_SOURCE -UNDEBUG -I. -Dgetifaddrs=downstream_getifaddrs -Dfreeifaddrs=downstream_freeifaddrs -Dup=downstream_original_up -Dipv4=downstream_original_ipv4 -Dipv6=downstream_original_ipv6 -c components/downstream-ip-original.c -o downstream-ip-original.o
gcc %{optflags} -std=c99 -D_DEFAULT_SOURCE -UNDEBUG -I. downstream-ip-regression.c downstream-ip-fixed.o downstream-ip-original.o util.o %{?build_ldflags} -o downstream-ip-regression
./downstream-ip-regression
python3 -I -B downstream-qa.py ./slstatus
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/slstatus
cmp slstatus.1 %{buildroot}%{_mandir}/man1/slstatus.1

%files
%license LICENSE
%doc README config.def.h
%{_bindir}/slstatus
%{_mandir}/man1/slstatus.1*

%files tests
%license LICENSE
%{_libexecdir}/slstatus-tests/

%changelog
* Tue Oct 20 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Package official stable source, preserve default configuration and test flag lifetime.
