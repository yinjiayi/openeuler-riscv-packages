# SPDX-License-Identifier: GPL-2.0-only AND MIT
Name:           corkscrew
Version:        2.0
Release:        1%{?dist}
Summary:        Tunnel a byte stream through an HTTP CONNECT proxy
License:        GPL-2.0-only
URL:            https://github.com/patpadgett/corkscrew
Source0:        corkscrew-2.0.tar.gz
Patch0:         0001-persistent-bounded-proxy-auth.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  automake
BuildRequires:  patch
BuildRequires:  coreutils
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  grep
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  bash
BuildRequires:  python3

%description
Corkscrew establishes an HTTP CONNECT tunnel and forwards a byte stream
between the proxy and standard input/output. Optional proxy credentials are
read from the original auth-file interface.

%package tests
Summary:        Installed-binary protocol checks for Corkscrew
License:        MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash

%description tests
Checks usage, authentication-file errors, HTTP CONNECT forwarding, proxy
credentials and rejection handling against bounded loopback-only test servers.
It makes no external proxy, Internet, security or performance acceptance claim.

%prep
%autosetup -p1 -n corkscrew-ae4802b09e1c022e416f9654970794fb9d7ac8a2
# Refresh only the obsolete 1999 architecture helpers, not configure or sources.
cp -p /usr/share/automake-1.16/config.guess config.guess
cp -p /usr/share/automake-1.16/config.sub config.sub
cat > downstream-qa.py <<'CORKSCREW_QA'
#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import argparse
import base64
import os
from pathlib import Path
import queue
import select
import signal
import socket
import subprocess
import tempfile
import threading
import time

def stop(process):
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=5)

def command(args, env, expected):
    process = subprocess.Popen(args, env=env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    try:
        out, err = process.communicate(timeout=10)
        assert process.returncode == expected, (args, process.returncode, out, err)
        return out, err
    finally:
        stop(process)

def proxy_case(binary, env, private, authenticated=False, reject=False):
    payload = b'client-binary\x00\xff\r\n'
    reply = b'proxy-binary\x00\xfe\r\n'
    expected = b'CONNECT qa.invalid:2222 HTTP/1.0'
    if authenticated:
        expected += b'\nProxy-Authorization: Basic ' + base64.b64encode(b'qa:secret')
    expected += b'\r\n\r\n'
    results = queue.Queue()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process = None
    worker = None
    try:
        server.bind(('127.0.0.1', 0))
        server.listen(1)
        server.settimeout(10)
        port = server.getsockname()[1]
        def serve():
            try:
                with server.accept()[0] as connection:
                    connection.settimeout(10)
                    request = bytearray()
                    while b'\r\n\r\n' not in request:
                        data = connection.recv(4096)
                        assert data
                        request.extend(data)
                        assert len(request) <= 8192
                    assert bytes(request) == expected, bytes(request)
                    if reject:
                        connection.sendall(b'HTTP/1.0 403 Forbidden\r\n\r\n')
                    else:
                        connection.sendall(b'HTTP/1.0 200 Connection established\r\n\r\n')
                        data = bytearray()
                        while len(data) < len(payload):
                            part = connection.recv(len(payload) - len(data))
                            assert part
                            data.extend(part)
                        assert bytes(data) == payload
                        connection.sendall(reply)
                results.put(None)
            except BaseException as error:
                results.put(error)
        worker = threading.Thread(target=serve, daemon=True)
        worker.start()
        args = [str(binary), '127.0.0.1', str(port), 'qa.invalid', '2222']
        if authenticated:
            auth = private / 'proxy-auth'
            auth.write_bytes(b'qa:secret\n')
            auth.chmod(0o600)
            args.append(str(auth))
        process = subprocess.Popen(args, env=env, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True)
        if reject:
            out, err = process.communicate(timeout=15)
            assert process.returncode == 255, (process.returncode, out, err)
            assert not out and b'Proxy could not open connnection to qa.invalid:' in err
        else:
            # Keep stdin open until the proxy closes; early EOF aborts upstream's loop.
            process.stdin.write(payload)
            process.stdin.flush()
            out = bytearray()
            deadline = time.monotonic() + 15
            while len(out) < len(reply) and time.monotonic() < deadline:
                if select.select([process.stdout], [], [], 0.1)[0]:
                    data = os.read(process.stdout.fileno(), 4096)
                    if not data:
                        break
                    out.extend(data)
            assert bytes(out) == reply, bytes(out)
            assert process.wait(timeout=5) == 0
            process.stdin.close()
            assert process.stdout.read() == b'' and process.stderr.read() == b''
        worker.join(timeout=12)
        assert not worker.is_alive(), 'proxy server deadline'
        error = results.get_nowait()
        assert error is None, repr(error)
    finally:
        if process is not None:
            stop(process)
            for pipe in (process.stdin, process.stdout, process.stderr):
                if pipe is not None and not pipe.closed:
                    pipe.close()
        server.close()
        if worker is not None:
            worker.join(timeout=12)
            assert not worker.is_alive(), 'proxy worker did not terminate'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', type=Path, default=Path('/usr/bin/corkscrew'))
    args = parser.parse_args()
    binary = args.binary.resolve(strict=True)
    assert binary.is_file() and os.access(binary, os.X_OK)
    with tempfile.TemporaryDirectory(prefix='corkscrew-qa-') as directory:
        private = Path(directory)
        env = {'PATH': '/usr/bin:/bin', 'HOME': str(private),
               'TMPDIR': str(private), 'LC_ALL': 'C'}
        out, err = command([str(binary)], env, 255)
        assert b'corkscrew 2.0 (agroman@agroman.net)' in out
        assert b'usage: corkscrew <proxyhost> <proxyport> <desthost> <destport> [authfile]' in out
        assert not err
        missing = private / 'absent-auth'
        out, err = command([str(binary), '127.0.0.1', '1', 'qa.invalid', '2222', str(missing)], env, 255)
        assert not out and ('Error opening ' + str(missing) + ':').encode() in err
        for name, data, diagnostic in (
                ('empty-auth', b'', b'Error reading proxy credentials from '),
                ('whitespace-auth', b' \t\n', b'Error reading proxy credentials from '),
                ('long-auth', b'A' * 5000 + b'\n', b'Proxy credentials exceed buffer limit in ')):
            invalid = private / name
            invalid.write_bytes(data)
            invalid.chmod(0o600)
            out, err = command([str(binary), '127.0.0.1', '1', 'qa.invalid', '2222', str(invalid)], env, 255)
            assert not out and diagnostic + str(invalid).encode() in err
            assert b"Couldn't establish connection" not in err
        proxy_case(binary, env, private)
        proxy_case(binary, env, private, authenticated=True)
        proxy_case(binary, env, private, reject=True)
    print('CORKSCREW_QA_PASS: usage, auth errors, CONNECT, binary forwarding, Basic header and rejection')

if __name__ == '__main__':
    main()
CORKSCREW_QA

%build
%configure
%make_build

%install
%make_install
install -d %{buildroot}%{_libexecdir}/corkscrew-tests
install -m 0755 downstream-qa.py %{buildroot}%{_libexecdir}/corkscrew-tests/installed-check.py

%check
make check
/usr/bin/python3 downstream-qa.py --binary "$PWD/corkscrew"

%files
%license COPYING
%doc README.markdown AUTHORS ChangeLog NEWS TODO
%{_bindir}/corkscrew

%files tests
%dir %{_libexecdir}/corkscrew-tests
%{_libexecdir}/corkscrew-tests/installed-check.py

%changelog
* Wed Oct 21 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 2.0-1
- Preserve default build/check/install and add target-only protocol checks.
- Keep authentication storage alive and reject empty or overlong credential input.
