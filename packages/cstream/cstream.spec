# SPDX-License-Identifier: MIT
Name:           cstream
Version:        4.0.0
Release:        1%{?dist}
Summary:        General purpose stream handling tool
License:        MIT
URL:            https://www.cons.org/cracauer/cstream.html
Source0:        cstream-4.0.0.tar.gz
Source1:        GPL-2.0.txt
Patch0:         patches/0001-preserve-listener-address-lifetime.patch
Patch1:         patches/0002-handle-pipe-hangup-in-poll-mode.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  gawk
BuildRequires:  coreutils
BuildRequires:  bash
BuildRequires:  python3
BuildRequires:  patch
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  jack-audio-connection-kit-devel

%description
cstream copies, buffers, limits and monitors streams, including regular files,
pipes and TCP connections. Default networking, resolver and sound probes are
preserved. Audio hardware and native throughput are not validated by this package.

%package tests
Summary:        Installed cstream functional checks
License:        MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash

%description tests
Target-only CLI, pipe, file, bounded concurrency and loopback checks against
the installed program. Original upstream make check remains in the build.

%prep
%autosetup -n cstream-%{version} -p1
cp -p %{SOURCE1} GPL-2.0.txt
cat > downstream-qa.py <<'CSTREAM_QA'
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
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import tempfile
import time

def stop(process):
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=10)

def finish(process, payload=None, status=0):
    try:
        out, err = process.communicate(input=payload, timeout=25)
    except BaseException:
        stop(process)
        raise
    assert process.returncode == status, (process.args, process.returncode, out, err)
    return out, err

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', required=True)
    args = parser.parse_args()
    binary = str(Path(args.binary).resolve(strict=True))
    env = dict(PATH='/usr/bin:/bin', LC_ALL='C', LANG='C', TERM='xterm')
    results = []
    with tempfile.TemporaryDirectory(prefix='cstream-qa-') as directory:
        work = Path(directory)
        env['HOME'] = str(work)
        def spawn(argv, input_pipe=True):
            return subprocess.Popen([binary, *argv], cwd=work, env=env,
                                    stdin=subprocess.PIPE if input_pipe else subprocess.DEVNULL,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    start_new_session=True)
        def run(argv, payload=b'', status=0):
            return finish(spawn(argv), payload, status)
        assert run(['-V'])[0] == b'4.0.0\n'
        results.append('version')
        for argv, status in [(['-?'], 1), (['-c', '5'], 1),
                             (['-b', '128', '-B', '64'], 1),
                             (['-i', 'missing-input'], 2)]:
            out, err = run(argv, status=status)
            assert err and not out, (argv, out, err)
        results.append('negative-cli')
        payload = bytes(range(256)) * 19 + b'\x00\xff\nend'
        for mode in range(5):
            out, err = run(['-c', str(mode), '-b', '128', '-B', '512'], payload)
            assert out == payload, (mode, len(out), err)
        results.append('all-concurrency-modes-and-pipe-eof')
        assert run(['-n', '513'], payload)[0] == payload[:513]
        assert len(run(['-i', '-', '-n', '1025'])[0]) == 1025
        assert run(['-o', '-'], payload)[0] == b''
        results.append('limit-generator-sink')
        source = work / 'source:data'
        destination = work / 'destination:data'
        source.write_bytes(payload)
        out, err = run(['-I', 'N', '-O', 'NF', '-i', source.name, '-o', destination.name])
        assert not out and destination.read_bytes() == payload, err
        results.append('private-colon-files-and-fsync')
        # Each listener owns a private loopback test. No external host is used.
        for family, host, six in [(socket.AF_INET, '127.0.0.1', '-1'),
                                  (socket.AF_INET6, '::1', '1')]:
            with socket.socket(family, socket.SOCK_STREAM) as reserve:
                reserve.bind((host, 0))
                port = reserve.getsockname()[1]
            process = spawn(['-6', six, '-i', ':' + str(port)], input_pipe=False)
            try:
                deadline = time.monotonic() + 10
                while True:
                    connection = socket.socket(family, socket.SOCK_STREAM)
                    connection.settimeout(10)
                    try:
                        connection.connect((host, port))
                        break
                    except ConnectionRefusedError:
                        connection.close()
                        assert process.poll() is None and time.monotonic() < deadline
                        time.sleep(0.05)
                with connection:
                    connection.sendall(payload)
                    connection.shutdown(socket.SHUT_WR)
                out, err = finish(process)
                assert out == payload, (family, out, err)
            finally:
                stop(process)
            with socket.socket(family, socket.SOCK_STREAM) as server:
                server.settimeout(15)
                server.bind((host, 0))
                server.listen(1)
                port = server.getsockname()[1]
                def receive():
                    with server.accept()[0] as peer:
                        peer.settimeout(15)
                        chunks = []
                        while True:
                            block = peer.recv(4096)
                            if not block:
                                return b''.join(chunks)
                            chunks.append(block)
                with ThreadPoolExecutor(max_workers=1) as executor:
                    received = executor.submit(receive)
                    out, err = run(['-6', six, '-o', host + ':' + str(port)], payload)
                    assert out == b'' and received.result(timeout=20) == payload, err
            results.append('ipv4-loopback' if family == socket.AF_INET else 'ipv6-loopback')
    print(json.dumps(dict(checks=results, result='PASS', scope='target functional; no native/performance/audio-device/isolation assurance'), sort_keys=True))

if __name__ == '__main__':
    main()
CSTREAM_QA

%build
%configure
%make_build

%install
%make_install
install -d %{buildroot}%{_libexecdir}/cstream-tests
install -m0755 downstream-qa.py %{buildroot}%{_libexecdir}/cstream-tests/installed-check.py

%check
%make_build check
python3 downstream-qa.py --binary ./cstream
python3 downstream-qa.py --binary %{buildroot}%{_bindir}/cstream

%files
%license COPYRIGHT GPL-2.0.txt
%doc README CHANGES INSTALLATION TODO
%{_bindir}/cstream
%{_mandir}/man1/cstream.1*

%files tests
%{_libexecdir}/cstream-tests/

%changelog
* Wed Oct 21 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 4.0.0-1
- Preserve default build/check/install and all original source notices.
- Correct listener address lifetime/accept capacity and mode4 pipe EOF.
- Add bounded target-only staged/installed functional checks.
