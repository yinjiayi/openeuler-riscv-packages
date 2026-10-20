# SPDX-License-Identifier: Apache-2.0
Name:           dhex
Version:        0.69
Release:        1%{?dist}
Summary:        Ncurses hexadecimal editor with a two-file diff mode
License:        GPL-2.0-or-later
URL:            https://www.dettus.net/dhex/
Source0:        dhex-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  ncurses-devel
BuildRequires:  ncurses-base
BuildRequires:  python3
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  tar
BuildRequires:  gzip

%description
Dhex is an ncurses hexadecimal editor with two-file difference viewing,
search logs, markers, a hexadecimal calculator and correlation tools.

%package tests
Summary:        Offline batch and PTY functional checks for Dhex
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash
Requires:       ncurses-base

%description tests
Authored downstream functional checks and the exact unchanged official source.
The upstream release has no original suite or test/check target.

%prep
%autosetup -n dhex_%{version} -p1
cat > downstream-qa.py <<'DHEX_QA'
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 yinjiayi. Licensed under the Apache License, Version 2.0.
"""Mandatory downstream functional checks, not an upstream or native suite."""
import errno
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import pty
import select
import struct
import subprocess
import sys
import tarfile
import tempfile
import termios
import time
import tty

root = Path(sys.argv[1]).resolve(strict=True)
binary = Path(sys.argv[2]).resolve(strict=True) if len(sys.argv) == 3 else root / 'usr/bin/dhex'
assert binary.is_file() and os.access(binary, os.X_OK)
assert sys.flags.isolated and sys.flags.dont_write_bytecode
elf = binary.read_bytes()[:20]
assert elf[:6] == b'\x7fELF\x02\x01' and int.from_bytes(elf[18:20], 'little') == 243
archive = root / 'usr/share/dhex/qa/dhex-0.69.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == '52730bcd1cf16bd4dae0de42531be9a4057535ec61ca38c0804eb8246ea6c41b'
with tarfile.open(archive, 'r:gz') as source:
    original = {m.name.split('/', 1)[1]: source.extractfile(m).read()
                for m in source.getmembers() if m.isfile()}
assert len(original) == 36
for package in ('dhex', 'dhex-tests'):
    for name in ('gpl.txt', 'README.txt'):
        assert (root / 'usr/share/licenses' / package / name).read_bytes() == original[name]
for name, section in (('dhex', '1'), ('dhexrc', '5'), ('dhex_markers', '5'), ('dhex_searchlog', '5')):
    manual = root / ('usr/share/man/man' + section) / (name + '.' + section)
    assert (manual.read_bytes() if manual.exists() else gzip.decompress(Path(str(manual) + '.gz').read_bytes())) == original[name + '.' + section]
checks = ['fixed-complete-source-notices-and-four-manuals']
with tempfile.TemporaryDirectory(prefix='dhex-qa-') as temporary:
    base = Path(temporary)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TERM': 'xterm-256color'}
    keys = ['KEYESC', *('KEYF' + str(i) for i in range(1, 11)),
            'KEYBACKSPACE', 'KEYDEL', 'KEYENTER', 'KEYTAB', 'KEYUP', 'KEYDOWN',
            'KEYRIGHT', 'KEYLEFT', 'KEYPGUP', 'KEYPGDOWN', 'KEYHOME', 'KEYEND']
    codes = {name: b'\x1b[' + str(101 + i).encode() + b'~' for i, name in enumerate(keys)}
    codes.update(KEYESC=b'\x1b\x1b', KEYENTER=b'\r', KEYTAB=b'\t', KEYF10=b'\x14')
    assert len(keys) == len(set(codes.values())) == 23
    config = base / 'keys.conf'
    config.write_text(''.join(name + ': ' + codes[name].hex() + '\n' for name in keys))
    def run(args, code=0):
        result = subprocess.run([str(binary), '-f', str(config), *args], cwd=base,
                                env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        assert result.returncode == code, (args, result.returncode, result.stdout, result.stderr)
        return result
    assert run(['-v']).stdout == b'0.69\n'
    assert b'General parameters' in run(['-h']).stderr
    assert run(['-g']).stdout == original['gpl.txt'] + b'\n'
    checks.append('version-help-and-embedded-license')
    data = b'.' * 8 + b'ABC' + b'.' * 13 + b'ABC' + b'.' * 13 + b'ABC' + b'.' * 21
    assert len(data) == 64
    (base / 'one').write_bytes(data)
    (base / 'two').write_bytes(data.replace(b'ABC', b'XYZ'))
    def offsets(name):
        lines = (base / name).read_text().splitlines()
        assert lines[:2] == ['#DHEX SEARCHLOG', '#VERSION 0']
        assert lines[3] == '#lines are all in hex'
        values = lines[4:]
        assert all(len(value) == 16 for value in values)
        return [int(value, 16) for value in values]
    run(['-sa', 'ABC', '-w', 'ascii.log', 'one'])
    assert offsets('ascii.log') == [8, 24, 40]
    run(['-sh', '41 42 43', '-w', 'hex.log', 'one'])
    assert offsets('hex.log') == [8, 24, 40]
    run(['-od', '63', '-sab', 'ABC', '-w', 'reverse.log', 'one'])
    assert offsets('reverse.log') == [40, 24, 8]
    run(['-sa', 'ABC', '-r', 'ascii.log', '-w', 'replay.log', 'one'])
    assert offsets('replay.log') == [8, 24, 40]
    run(['-ad', '4096', '-sa', 'ABC', '-w', 'base.log', 'one'])
    assert offsets('base.log') == [4104, 4120, 4136]
    run(['-s1a', 'ABC', '-w1', 'left.log', '-s2h', '58595a', '-w2', 'right.log', 'one', 'two'])
    assert offsets('left.log') == offsets('right.log') == [8, 24, 40]
    run(['-sa', 'absent', '-w', 'absent.log', 'one'])
    assert offsets('absent.log') == []
    assert (base / 'one').read_bytes() == data
    assert (base / 'two').read_bytes() == data.replace(b'ABC', b'XYZ')
    assert b'error opening inputfile' in run(['missing-file'], 1).stderr
    assert b'unknown correlation algorithm' in run(['-cz'], 1).stderr
    checks.append('ascii-hex-reverse-replay-base-dual-absent-search-and-input-failures')

    class Terminal:
        def __init__(self, args):
            self.master, slave = pty.openpty()
            tty.setraw(slave)
            fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, 80, 0, 0))
            try:
                self.child = subprocess.Popen([str(binary), '-f', str(config), *args],
                    cwd=base, env=env, stdin=slave, stdout=slave, stderr=slave, close_fds=True)
            finally:
                os.close(slave)
            self.output = bytearray()
        def read_until(self, predicate, start=0):
            deadline = time.monotonic() + 20
            while not predicate(bytes(self.output[start:])):
                assert len(self.output) < 2 * 1024 * 1024, 'terminal output bound'
                remaining = deadline - time.monotonic()
                assert remaining > 0, ('terminal deadline', bytes(self.output[-300:]))
                ready, _, _ = select.select([self.master], [], [], remaining)
                assert ready, 'terminal readiness deadline'
                try:
                    part = os.read(self.master, 65536)
                except OSError as error:
                    if error.errno == errno.EIO:
                        part = b''
                    else:
                        raise
                assert part, ('unexpected terminal EOF', self.child.poll(), bytes(self.output[-300:]))
                self.output.extend(part)
        def key(self, value):
            start = len(self.output)
            assert os.write(self.master, value) == len(value)
            self.read_until(bool, start)
        def finish(self):
            # Drain bounded terminal output concurrently so wait cannot deadlock.
            deadline = time.monotonic() + 20
            while self.child.poll() is None:
                assert time.monotonic() < deadline, 'terminal exit deadline'
                ready, _, _ = select.select([self.master], [], [], min(0.2, deadline - time.monotonic()))
                if ready:
                    try:
                        part = os.read(self.master, 65536)
                    except OSError as error:
                        if error.errno != errno.EIO:
                            raise
                        part = b''
                    self.output.extend(part)
                    assert len(self.output) < 2 * 1024 * 1024
            assert self.child.wait(timeout=1) == 0
        def close(self):
            if self.child.poll() is None:
                self.child.kill()
                self.child.wait(timeout=5)
            os.close(self.master)
    def edit_case(name, action, expected):
        path = base / name
        path.write_bytes(b'0123456789abcdef')
        terminal = Terminal([name])
        try:
            terminal.read_until(lambda output: name.encode() in output and b'Quit' in output)
            terminal.key(b'4')
            terminal.key(b'1')
            if action == 'undo':
                terminal.key(codes['KEYF9'])
            os.write(terminal.master, codes['KEYF10'])
            if action != 'undo':
                terminal.read_until(lambda output: b'Save changes?' in output)
                assert os.write(terminal.master, b'y' if action == 'save' else b'n') == 1
            terminal.finish()
        finally:
            terminal.close()
        assert path.read_bytes() == expected, (name, path.read_bytes())
    edit_case('edit-save', 'save', b'A123456789abcdef')
    edit_case('edit-undo', 'undo', b'0123456789abcdef')
    edit_case('edit-discard', 'discard', b'0123456789abcdef')
    terminal = Terminal(['one', 'two'])
    try:
        terminal.read_until(lambda output: b'one' in output and b'two' in output and b'Corr.' in output)
        terminal.key(codes['KEYF3'])
        terminal.key(codes['KEYF4'])
        os.write(terminal.master, codes['KEYF10'])
        terminal.finish()
    finally:
        terminal.close()
    assert (base / 'one').read_bytes() == data
    assert (base / 'two').read_bytes() == data.replace(b'ABC', b'XYZ')
    checks.append('mandatory-pty-hex-save-undo-discard-and-diff-navigation')
print('DHEX_QA_OK ' + json.dumps(checks))
DHEX_QA

%build
# Keep the original 13-object all target, includes and ncurses link.
%make_build CC=gcc CFLAGS='%{build_cflags} -Wall' LDFLAGS='%{build_ldflags} -L/usr/lib -L/usr/local/lib -L/usr/lib/ncurses -L/usr/local/lib/ncurses'

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_prefix}/man/man1 %{buildroot}%{_prefix}/man/man5 %{buildroot}%{_mandir}
# Upstream DESTDIR is a prefix and the default install strips dhex; retain it.
make install DESTDIR=%{buildroot}%{_prefix}
mv %{buildroot}%{_prefix}/man/man1 %{buildroot}%{_mandir}/
mv %{buildroot}%{_prefix}/man/man5 %{buildroot}%{_mandir}/
rmdir %{buildroot}%{_prefix}/man
for package in %{name} %{name}-tests; do
    install -Dm 0644 gpl.txt %{buildroot}%{_licensedir}/$package/gpl.txt
    install -Dm 0644 README.txt %{buildroot}%{_licensedir}/$package/README.txt
done
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# New mandatory downstream QA; upstream has no test/check target to invoke.
/usr/bin/python3 -I -B downstream-qa.py %{buildroot} "$PWD/dhex"
/usr/bin/python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/gpl.txt %{_licensedir}/%{name}/README.txt
%{_bindir}/dhex
%{_mandir}/man1/dhex.1*
%{_mandir}/man5/dhexrc.5*
%{_mandir}/man5/dhex_markers.5*
%{_mandir}/man5/dhex_searchlog.5*

%files tests
%license %{_licensedir}/%{name}-tests/gpl.txt %{_licensedir}/%{name}-tests/README.txt
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Tue Oct 20 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.69-1
- Preserve the original default build, full source notices and four manuals.
- Add mandatory offline batch and PTY functional QA without an upstream-suite claim.
