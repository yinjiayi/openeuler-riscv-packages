# SPDX-License-Identifier: MIT
Name:           qprint
Version:        1.1
Release:        1%{?dist}
Summary:        Quoted-printable encoder and decoder
License:        LicenseRef-Public-Domain
URL:            https://www.fourmilab.ch/webtools/qprint/
Source0:        qprint-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  bash
BuildRequires:  python3

%description
Encode and decode MIME quoted-printable data, with binary, paranoid and
EBCDIC-compatible modes. Preserve the original generated C default build.

%package tests
License:        LicenseRef-Public-Domain AND MIT AND FSFUL
Summary:        Qprint unchanged source and installed functional tests
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       make
Requires:       coreutils
Requires:       diffutils
Requires:       bash

%description tests
Complete original distribution and downstream target-only checks, including
both unchanged upstream check and wringer recipes against installed qprint.

%prep
%autosetup -n qprint-%{version} -p1
# Upstream README permits refreshing generated C timestamps, not regeneration.
touch qprint.c wretch.c
cat > downstream-qa.py <<'QPRINT_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi. Downstream packaging QA, not upstream code.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Target-only upstream recipe replay plus bytewise/CLI functional checks."""
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import signal
import subprocess
import sys
import tarfile
import tempfile

assert sys.flags.isolated and sys.flags.dont_write_bytecode
mode, argument = sys.argv[1:]
assert mode in ('--build', '--installed')
checks = []
with tempfile.TemporaryDirectory(prefix='qprint-qa-') as temporary:
    base = Path(temporary)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(base), 'SHELL': '/bin/sh'}
    def run(args, data=None, code=0, cwd=base, timeout=30):
        process = subprocess.Popen(list(map(str, args)), cwd=cwd, env=env,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True)
        try:
            stdout, stderr = process.communicate(data, timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate(timeout=5)
            raise AssertionError(('deadline', args, stdout[-4096:], stderr[-4096:]))
        assert process.returncode == code, (args, process.returncode, stdout, stderr)
        return stdout, stderr
    if mode == '--build':
        work = Path(argument).resolve(strict=True)
        binary = work / 'qprint'
        makefile = (work / 'Makefile').read_bytes()
        # Force the original target generator, not the distributed fixture.
        (work / 'wretch.bin').unlink(missing_ok=True)
        make_options = []
    else:
        root = Path(argument).resolve(strict=True)
        binary = root / 'usr/bin/qprint'
        archive = root / 'usr/share/qprint/qa/qprint-1.1.tar.gz'
        assert hashlib.sha256(archive.read_bytes()).hexdigest() == 'ffa9ca1d51c871fb3b56a4bf0165418348cf080f01ff7e59cd04511b9665019c'
        work = base / 'source'; work.mkdir()
        original = {}
        with tarfile.open(archive, 'r:gz') as source:
            members = source.getmembers()
            assert len(members) == 23 and sum(member.isfile() for member in members) == 22
            for member in members:
                path = PurePosixPath(member.name)
                assert path.parts[0] == 'qprint-1.1' and '..' not in path.parts and not path.is_absolute()
                if member.isdir():
                    assert len(path.parts) == 1
                    continue
                assert member.isfile() and len(path.parts) == 2 and member.size <= 1048576
                data = source.extractfile(member).read()
                original[path.name] = data
                (work / path.name).write_bytes(data)
        manual = root / 'usr/share/man/man1/qprint.1'
        assert (manual.read_bytes() if manual.is_file() else gzip.decompress(manual.with_suffix('.1.gz').read_bytes())) == original['qprint.1']
        for package in ('qprint', 'qprint-tests'):
            assert (root / 'usr/share/licenses' / package / 'COPYING').read_bytes() == original['COPYING']
        for name in ('README', 'INSTALL', 'index.html', 'logo.gif', 'qprint.pdf', 'rfc1521.txt', 'rfc1521.html'):
            assert (root / 'usr/share/doc/qprint' / name).read_bytes() == original[name]
        (work / 'qprint').symlink_to(binary)
        makefile = original['Makefile.in']
        make_options = ['-o', 'qprint', '-o', 'wretch.bin', 'PRODUCT=qprint']
        checks.append('installed-source-manual-docs-notices')
    assert binary.is_file() and os.access(binary, os.X_OK)
    private = base / 'upstream-tmp'; private.mkdir()
    assert b'/tmp/' in makefile
    adapted = makefile.replace(b'/tmp/', (str(private) + '/').encode())
    assert adapted.replace((str(private) + '/').encode(), b'/tmp/') == makefile
    test_makefile = base / 'Makefile.tests'; test_makefile.write_bytes(adapted)
    output, error = run(['/usr/bin/make', '-f', test_makefile, *make_options, 'check', 'wringer'],
                        cwd=work, timeout=300)
    print(output.decode('utf-8', 'backslashreplace'), end='')
    print(error.decode('utf-8', 'backslashreplace'), file=sys.stderr, end='')
    assert b'All tests passed.' in output and b'Wringer test passed.' in output
    assert b'test failed' not in output.lower() and b'test failed' not in error.lower()
    assert hashlib.sha256((work / 'wretch.bin').read_bytes()).hexdigest() == 'b4f06c6d99623e87ffd32aadd8e9f9b8a289dc54d10f85d5865851b861c32343'
    checks.append('original-check-and-thirteen-level-wringer')
    def command(args, data=b'', code=0):
        return run([binary, *args], data, code)
    assert b'qprint 1.1' in command(['--version'])[0]
    assert b'Quoted-Printable' in command(['--help'])[0]
    assert b'public domain' in command(['--copyright'])[0]
    for data in (b'', bytes(range(256)), bytes(range(255, -1, -1)) * 5,
                 b'A' * 4096 + b'\x00\xff\r\n\t '):
        for options in (['-eb'], ['-ebp'], ['-ebi']):
            encoded, _ = command(options, data)
            assert command(['-d'], encoded)[0] == data
            assert all(len(line) <= 72 for line in encoded.split(b'\r\n'))
    assert command(['-e'], b'one\rtwo\nthree\r\nfour\n\r')[0] == b'one\r\ntwo\r\nthree\r\nfour\r\n'
    assert command(['-d'], b'one\rtwo\nthree\r\nfour\n\r')[0] == b'one\ntwo\nthree\nfour\n'
    assert command(['-d'], b'=00=ff=0a=0D')[0] == b'\x00\xff\n\r'
    assert command(['-eb'], b'=\x00\xff')[0] == b'=3D=00=FF=\r\n'
    assert command(['-ebi'], b'!"#$@[\\]^`{|}~')[0].replace(b'=\r\n', b'') == b'=21=22=23=24=40=5B=5C=5D=5E=60=7B=7C=7D=7E'
    checks.append('binary-paranoid-ebcdic-eol-long-lines-pipes')
    input_file = base / 'input'; encoded_file = base / 'encoded'; decoded_file = base / 'decoded'
    input_file.write_bytes(bytes(range(256)))
    command(['-eb', input_file, encoded_file])
    command(['-d', encoded_file, decoded_file])
    assert decoded_file.read_bytes() == input_file.read_bytes()
    command([], code=2)
    command(['-ed'], code=2)
    command(['-e', base / 'missing'], code=2)
    command(['-e', input_file, encoded_file, decoded_file], code=2)
    assert b'bad equal sign escape' in command(['-d'], b'=GG', code=1)[1]
    assert command(['-dn'], b'=GG', code=1)[1] == b''
    checks.append('file-arguments-and-negative-status-diagnostics')
print(json.dumps({'phase': mode, 'checks': checks, 'source_archive_unchanged': mode == '--installed'}))
QPRINT_QA

%build
%configure
%make_build

%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
%make_install INSTALL_PROGRAM='install -p -m755'
install -D -m0644 %{SOURCE0} %{buildroot}%{_datadir}/qprint/qa/qprint-%{version}.tar.gz
install -D -m0644 downstream-qa.py %{buildroot}%{_libexecdir}/qprint-tests/qa.py
# Make staged checks inspect exactly the final docs/licenses, before file processing.
install -d %{buildroot}%{_docdir}/qprint
install -p -m0644 README INSTALL index.html logo.gif qprint.pdf rfc1521.txt rfc1521.html %{buildroot}%{_docdir}/qprint/
install -D -m0644 COPYING %{buildroot}%{_licensedir}/qprint/COPYING
install -D -m0644 COPYING %{buildroot}%{_licensedir}/qprint-tests/COPYING

%check
/usr/bin/python3 -I -B downstream-qa.py --build "$PWD"
/usr/bin/python3 -I -B downstream-qa.py --installed %{buildroot}

%files
%license %{_licensedir}/qprint/
%doc %{_docdir}/qprint/
%{_bindir}/qprint
%{_mandir}/man1/qprint.1*

%files tests
%license %{_licensedir}/qprint-tests/
%{_libexecdir}/qprint-tests/
%{_datadir}/qprint/

%changelog
* Wed Oct 21 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1-1
- Preserve default build/install and both complete original test targets.
