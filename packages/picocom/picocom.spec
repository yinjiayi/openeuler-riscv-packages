# SPDX-License-Identifier: GPL-2.0-or-later
Name:           picocom
Version:        3.1
Release:        1%{?dist}
Summary:        Minimal serial-port terminal emulator
License:        GPL-2.0-or-later AND BSD-2-Clause
URL:            https://github.com/npat-efault/picocom
Source0:        picocom-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  python3
BuildRequires:  bash
BuildRequires:  lrzsz
Requires:       lrzsz

%description
Picocom is a minimal serial-port terminal emulator with character mappings,
logging, file-transfer command integration and vendored linenoise editing.

%package tests
Summary:        Picocom unchanged source and installed functional checks
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3
Requires:       bash

%description tests
Complete unchanged upstream source and downstream target-only functional QA.
Upstream provides no automated test/check Makefile target.

%prep
%autosetup -n picocom-90385aabe2b51f39fa130627d46b377569f82d4a -p1
cat > downstream-qa.py <<'PICOCOM_QA'
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright 2026 yinjiayi. Distributed under GPL2-or-later, source LICENSE.txt.
"""Authored target-only QA, not an upstream suite or physical serial test."""
import fcntl
import gzip
import hashlib
import os
from pathlib import Path
import select
import signal
import struct
import subprocess
import sys
import tarfile
import tempfile
import termios
import time

assert sys.flags.isolated and sys.flags.dont_write_bytecode
root = Path(sys.argv[1]).resolve(strict=True)
archive = root / 'usr/share/picocom/qa/picocom-3.1.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == 'a38f431d27b6c6275b0c281c7d53f0bfc7bf22d251122d53a56fb407457e2054'
with tarfile.open(archive, 'r:gz') as source:
    original = {member.name.split('/', 1)[1]: source.extractfile(member).read()
                for member in source.getmembers() if member.isfile()}
assert len(original) == 40
binary = root / 'usr/bin/picocom'
assert binary.is_file() and os.access(binary, os.X_OK)
for command in ('sz', 'rz'):
    assert Path('/usr/bin', command).is_file() and os.access('/usr/bin/' + command, os.X_OK)
manual = root / 'usr/share/man/man1/picocom.1'
actual = manual.read_bytes() if manual.is_file() else gzip.decompress(manual.with_suffix('.1.gz').read_bytes())
assert actual == original['picocom.1']
for package in ('picocom', 'picocom-tests'):
    for installed, source_name in (('LICENSE.txt', 'LICENSE.txt'), ('LICENSE', 'linenoise-1.0/LICENSE')):
        assert (root / 'usr/share/licenses' / package / installed).read_bytes() == original[source_name]
for name in ('README.md', 'CONTRIBUTORS', 'CHANGES.old', 'TODO', 'bsd_notes.txt', 'lowerrts.md',
             'picocom.1.md', 'picocom.1.html', 'picocom.1.pdf', 'pcasc', 'pcxm', 'pcym', 'pczm'):
    assert (root / 'usr/share/doc/picocom' / name).read_bytes() == original[name]
checks = ['installed-full-source-manual-docs-both-license-texts-default-command-providers']
with tempfile.TemporaryDirectory(prefix='picocom-qa-') as temporary:
    base = Path(temporary)
    home = base / 'home'; home.mkdir()
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(home), 'TERM': 'xterm', 'SHELL': '/bin/sh'}
    def batch(args, success=True):
        result = subprocess.run([str(binary), *map(str, args)], cwd=base, env=env,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=15, start_new_session=True)
        assert (result.returncode == 0) == success, (args, result.returncode, result.stdout, result.stderr)
        return result.stdout + result.stderr
    help_text = batch(['--help'])
    for token in (b'picocom v3.1', b'TTY_Q_SZ is 0', b'HIGH_BAUD is enabled',
                  b'USE_FLOCK is enabled', b'LINENOISE is enabled', b'HISTFILE is: .picocom_history'):
        assert token in help_text, (token, help_text)
    checks.append('help-default-build-features-no-custombaud-or-hardware-claim')
    for args, diagnostic in (([], b'No port given'), (['--bad-option'], b'Unrecognized option(s)'),
                             (['--baud', '0'], b'Invalid --baud'), (['--flow', '?'], b'Invalid --flow'),
                             (['--parity', '?'], b'Invalid --parity'), (['--databits', '9'], b'Invalid --databits'),
                             (['--stopbits', '3'], b'Invalid --stopbits'), (['--imap', 'invalid'], b'Invalid --imap'),
                             (['--exit-after', '-1'], b'Inavild --exit-after'),
                             (['--raise-rts', '--lower-rts'], b'Both --raise-rts and --lower-rts given')):
        assert diagnostic in batch(args, False), (args, diagnostic)
    checks.append('negative-cli-validation')
    def read_until(fd, token, process, timeout=12):
        data = bytearray(); deadline = time.monotonic() + timeout
        while token not in data:
            assert time.monotonic() < deadline, ('PTY deadline', token, bytes(data), process.poll())
            ready, _, _ = select.select([fd], [], [], min(0.2, max(0, deadline-time.monotonic())))
            if not ready:
                assert process.poll() is None, ('premature exit', process.returncode, bytes(data))
                continue
            try:
                chunk = os.read(fd, 65536)
            except OSError as error:
                raise AssertionError(('PTY read failed', error, process.poll(), bytes(data))) from error
            assert chunk, ('PTY EOF', bytes(data), process.poll())
            data.extend(chunk)
            assert len(data) <= 1048576
        return bytes(data)
    def cleanup(process, descriptors):
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
        for descriptor in descriptors:
            os.close(descriptor)
    # Immediate exit still sends its complete init-string; it needs no user TTY.
    serial_master, serial_slave = os.openpty()
    try:
        data = batch(['--noreset', '--exit', '--initstring', 'PICOCOM-init', os.ttyname(serial_slave)])
        assert b'Terminal ready' in data and b'Thanks for using picocom' in data
        ready, _, _ = select.select([serial_master], [], [], 5)
        assert ready and os.read(serial_master, 4096) == b'PICOCOM-init'
    finally:
        os.close(serial_master); os.close(serial_slave)
    checks.append('init-string-immediate-exit')
    for mapped in (False, True):
        control_master, control_slave = os.openpty()
        serial_master, serial_slave = os.openpty()
        descriptors = (control_master, control_slave, serial_master, serial_slave)
        process = None
        try:
            fcntl.ioctl(control_slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, 100, 0, 0))
            log = base / ('mapped.log' if mapped else 'raw.log')
            args = [str(binary), '--noreset', '--logfile', str(log)]
            if mapped:
                args += ['--imap', 'lfcrlf', '--omap', 'crcrlf']
            args.append(os.ttyname(serial_slave))
            process = subprocess.Popen(args, cwd=base, env=env, stdin=control_slave,
                                       stdout=control_slave, stderr=control_slave, start_new_session=True)
            startup = read_until(control_master, b'Terminal ready\r\n', process)
            for token in (b'baudrate is    : 9600', b'local echo is  : no', b'nolock is      : no',
                          b'send_cmd is    : sz -vv', b'receive_cmd is : rz -vv -E'):
                assert token in startup, (token, startup)
            outgoing = b'outgoing-\x00\xff\rEND'
            expected = outgoing.replace(b'\r', b'\r\n') if mapped else outgoing
            os.write(control_master, outgoing)
            assert read_until(serial_master, expected, process) == expected
            incoming = b'incoming-\x00\xfe\nEND'
            expected = incoming.replace(b'\n', b'\r\n') if mapped else incoming
            os.write(serial_master, incoming)
            assert read_until(control_master, expected, process) == expected
            os.write(control_master, b'\x01\x18')
            read_until(control_master, b'Thanks for using picocom\r\n', process)
            assert process.wait(timeout=5) == 0
            assert log.read_bytes() == incoming
        finally:
            cleanup(process, descriptors)
        checks.append('mapped-PTY-transfer-log-command-exit' if mapped else 'default-binary-PTY-transfer-log-command-exit')
print('picocom downstream QA passed: ' + ', '.join(checks))
PICOCOM_QA

%build
# Keep original feature CPPFLAGS, seven objects and original default all target.
%make_build CC="%{__cc}" CFLAGS="%{optflags} -Wall -g" LDFLAGS="%{?build_ldflags} -g"

%install
# README's original installation: copy binary and shipped manual, no early strip.
install -Dpm0755 picocom %{buildroot}%{_bindir}/picocom
install -Dpm0644 picocom.1 %{buildroot}%{_mandir}/man1/picocom.1
install -Dpm0644 downstream-qa.py %{buildroot}%{_libexecdir}/picocom-tests/qa.py
install -Dpm0644 %{SOURCE0} %{buildroot}%{_datadir}/picocom/qa/picocom-%{version}.tar.gz
# Install notices/docs before %%check, rather than relying on later %%files copying.
install -d %{buildroot}%{_licensedir}/picocom %{buildroot}%{_licensedir}/picocom-tests %{buildroot}%{_docdir}/picocom
for package in picocom picocom-tests; do
    install -pm0644 LICENSE.txt %{buildroot}%{_licensedir}/$package/LICENSE.txt
    install -pm0644 linenoise-1.0/LICENSE %{buildroot}%{_licensedir}/$package/LICENSE
done
install -pm0644 README.md CONTRIBUTORS CHANGES.old TODO bsd_notes.txt lowerrts.md picocom.1.md picocom.1.html picocom.1.pdf pcasc pcxm pcym pczm %{buildroot}%{_docdir}/picocom/

%check
%{__python3} -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/picocom/
%doc %{_docdir}/picocom/
%{_bindir}/picocom
%{_mandir}/man1/picocom.1*

%files tests
%license %{_licensedir}/picocom-tests/
%{_libexecdir}/picocom-tests/
%{_datadir}/picocom/

%changelog
* Wed Oct 21 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 3.1-1
- Preserve upstream default serial-terminal build and add target-only installed QA.
