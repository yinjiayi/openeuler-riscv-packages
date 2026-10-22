# SPDX-License-Identifier: GPL-3.0-or-later AND MIT
Name:           mdp
Version:        1.0.19
Release:        1%{?dist}
Summary:        Markdown presentations in a terminal
License:        GPL-3.0-or-later
URL:            https://github.com/visit1985/mdp
Source0:        mdp-1.0.19.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  ncurses-devel
BuildRequires:  coreutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  bash
BuildRequires:  python3
Requires:       ncurses-base

%description
mdp displays Markdown presentations in an ncurses terminal, including slide
navigation, metadata, inline formatting, comments and resize recovery.

%package tests
Summary:        Installed-binary checks and original PTY suites for mdp
License:        GPL-3.0-or-later AND MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash
Requires:       ncurses-base

%description tests
Retains the complete original source and runs both unchanged upstream PTY
test suites against the installed binary, plus CLI and payload checks.

%prep
%autosetup -n mdp-1bd179043ca4f21705ebe89e57c1c5b80101e7d7
cat > downstream-qa.py <<'MDP_QA'
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
import hashlib
import os
from pathlib import Path, PurePosixPath
import signal
import subprocess
import tarfile
import tempfile

ARCHIVE_SHA = '59fc010403f63a425b7b31f8b3a6bd8adc6898fcf5349fb9720fdc9b94e893be'
ROOT = 'mdp-1bd179043ca4f21705ebe89e57c1c5b80101e7d7'
SUITES = [('test_comments.py', b'15/15 checks passed.'),
          ('test_resize.py', b'9/9 checks passed.')]

def run(args, cwd, env, status=0, timeout=180):
    process = subprocess.Popen(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    try:
        out, err = process.communicate(timeout=timeout)
    except BaseException:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise
    print(out.decode('utf-8', 'backslashreplace'), end='')
    print(err.decode('utf-8', 'backslashreplace'), end='')
    assert process.returncode == status, (args, process.returncode, out, err)
    return out, err

def full_suites(work, binary, env, build):
    if build:
        command = ['/usr/bin/make', 'test', 'CC=' + os.environ['MDP_RPM_CC'],
                   'CFLAGS=' + os.environ['MDP_RPM_CFLAGS'],
                   'LDFLAGS=' + os.environ['MDP_RPM_LDFLAGS']]
        out, err = run(command, work, env)
        lines = [line.strip() for line in out.splitlines()]
        for _, summary in SUITES:
            assert lines.count(summary) == 1
        assert not any(line.startswith(b'FAIL:') for line in lines + err.splitlines())
    else:
        assert not (work / 'mdp').exists()
        (work / 'mdp').symlink_to(binary)
        for suite, summary in SUITES:
            out, err = run(['/usr/bin/python3', str(work / 'tests' / suite)], work, env)
            lines = [line.strip() for line in out.splitlines()]
            assert lines.count(summary) == 1
            assert not any(line.startswith(b'FAIL:') for line in lines + err.splitlines())

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--build', type=Path)
    group.add_argument('--installed', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='mdp-qa-') as directory:
        private = Path(directory)
        env = {'PATH': '/usr/bin:/bin', 'HOME': str(private), 'TMPDIR': str(private),
               'TERM': 'xterm', 'LC_ALL': 'C.UTF-8'}
        if args.build:
            work = args.build.resolve()
            binary = work / 'mdp'
        else:
            binary = Path('/usr/bin/mdp')
            archive = Path('/usr/share/mdp-tests/source.tar.gz')
            assert hashlib.sha256(archive.read_bytes()).hexdigest() == ARCHIVE_SHA
            count = 0
            with tarfile.open(archive, 'r:gz') as source:
                for member in source.getmembers():
                    path = PurePosixPath(member.name)
                    assert not path.is_absolute() and '..' not in path.parts and path.parts[0] == ROOT
                    assert member.isdir() or member.isfile()
                    target = private.joinpath(*path.parts)
                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        assert member.size <= 1000000
                        stream = source.extractfile(member)
                        assert stream is not None
                        data = stream.read()
                        assert len(data) == member.size
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(data)
                        count += 1
            assert count == 33
            work = private / ROOT
        assert binary.is_file() and os.access(binary, os.X_OK)
        out, err = run([str(binary), '--version'], work, env, timeout=15)
        assert out.splitlines()[0] == b'mdp 1.0.19' and b'GPLv3+' in out
        out, err = run([str(binary), '--help'], work, env, status=1, timeout=15)
        assert b'Usage: mdp [OPTION]... [FILE]' in err
        out, err = run([str(binary), '--jump', 'not-a-number'], work, env, status=1, timeout=15)
        assert b'invalid numeric value for --jump' in err
        out, err = run([str(binary), str(private / 'absent.md')], work, env, status=1, timeout=15)
        assert b'No such file or directory' in err
        full_suites(work, binary, env, bool(args.build))
        if args.installed:
            assert Path('/usr/share/licenses/mdp/COPYING').is_file()
            assert Path('/usr/share/licenses/mdp-tests/COPYING').is_file()
            assert Path('/usr/share/doc/mdp/sample.md').is_file()
            assert Path('/usr/share/man/man1/mdp.1').is_file() or Path('/usr/share/man/man1/mdp.1.gz').is_file()
        print('mdp downstream installed/build checks passed; original 24 PTY checks retained')

if __name__ == '__main__':
    main()
MDP_QA

%build
%make_build CC="%{__cc}" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
%make_install PREFIX=%{_prefix}
install -d %{buildroot}%{_libexecdir}/mdp-tests %{buildroot}%{_datadir}/mdp-tests
install -m 0755 downstream-qa.py %{buildroot}%{_libexecdir}/mdp-tests/installed-check.py
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/mdp-tests/source.tar.gz

%check
MDP_RPM_CC="%{__cc}" MDP_RPM_CFLAGS="%{optflags} -Wall" MDP_RPM_LDFLAGS="%{?build_ldflags}" /usr/bin/python3 downstream-qa.py --build "$PWD"

%files
%license COPYING
%doc README.md AUTHORS CREDITS sample.md docs
%{_bindir}/mdp
%{_mandir}/man1/mdp.1*

%files tests
%license COPYING
%dir %{_libexecdir}/mdp-tests
%{_libexecdir}/mdp-tests/installed-check.py
%dir %{_datadir}/mdp-tests
%{_datadir}/mdp-tests/source.tar.gz

%changelog
* Wed Oct 21 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.0.19-1
- Preserve default build/install and both full upstream PTY suites for RISC-V.
