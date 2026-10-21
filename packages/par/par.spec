# SPDX-License-Identifier: MIT
# Upstream's protoMakefile has empty CFLAGS/CPPFLAGS and no debug generation.
# Do not add -g and then describe the original defaults as unchanged.
%global debug_package %{nil}
Name:           par
Version:        1.53.0
Release:        1%{?dist}
Summary:        Paragraph reformatter
License:        MIT
URL:            http://www.nicemice.net/par/
Source0:        par-1.53.0-eb0590f6bafc.zip

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  bash
BuildRequires:  python3
BuildRequires:  glibc-common
BuildRequires:  glibc-locale-source
BuildRequires:  unzip
BuildRequires:  gzip

%description
Par reformats paragraphs while preserving meaningful prefixes and suffixes.
The original default compiler, empty flags, five-object build, documentation,
and complete 39-case POSIX-shell test suite are retained without source patches.

%package tests
Summary:        Original Par fixtures and installed functional checks
License:        MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash
Requires:       coreutils
Requires:       glibc-common
Requires:       glibc-locale-source

%description tests
All 39 original inline fixtures, including en_US ISO-8859-1 and he_IL
ISO-8859-8 locale cases, plus target-only functional checks. Tests have not
been run on the packaging host. QEMU results are not native hardware proof.

%prep
%setup -q -n amc-nicemice-par-eb0590f6bafc
cat > downstream-qa.py <<'PAR_QA'
#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile

TEST_SHA = '75ba2f1c356a767849edd8785098343286692f8ed11723a23084cbf639bf69c3'

def command(argv, env, cwd, payload=None, status=0, timeout=300):
    process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=True)
    try:
        out, err = process.communicate(payload, timeout=timeout)
    except BaseException:
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        process.wait(timeout=15)
        raise
    assert process.returncode == status, (argv, process.returncode, out, err)
    return out, err

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', required=True)
    parser.add_argument('--suite', required=True)
    parser.add_argument('--make-default-test', action='store_true')
    args = parser.parse_args()
    binary = str(Path(args.binary).resolve(strict=True))
    suite = Path(args.suite).resolve(strict=True)
    assert hashlib.sha256(suite.read_bytes()).hexdigest() == TEST_SHA
    assert suite.read_bytes().startswith(b':\n')
    with tempfile.TemporaryDirectory(prefix='par-qa-') as directory:
        work = Path(directory)
        env = dict(PATH='/usr/bin:/bin', LC_ALL='C', LANG='C', HOME=str(work))
        locales = work / 'locales'
        locales.mkdir()
        # Require actual successful locale generation and matching charmaps;
        # no fallback to C/UTF8 is accepted as coverage of legacy locale cases.
        for name, charmap in [('en_US', 'ISO-8859-1'), ('he_IL', 'ISO-8859-8')]:
            command(['/usr/bin/localedef', '-f', charmap, '-i', name,
                     str(locales / name)], env, work)
            locale_env = dict(env, LOCPATH=str(locales), LC_ALL=name)
            out, err = command(['/usr/bin/locale', 'charmap'], locale_env, work)
            assert out == (charmap + '\n').encode() and not err, (name, out, err)
        old_tmp = set(Path('/tmp').glob('test-par-*'))
        assert not old_tmp, ('stale original-suite temporary state', sorted(map(str, old_tmp)))
        if args.make_default_test:
            assert (suite.parent / 'par').resolve(strict=True) == Path(binary)
            argv = ['/usr/bin/make', '-f', 'protoMakefile', 'test']
        else:
            # The original script intentionally has no shebang. Explicit sh
            # preserves its bytes and avoids direct-exec ENOEXEC.
            argv = ['/bin/sh', str(suite), binary]
        out, err = command(argv, env, suite.parent, timeout=600)
        print(out.decode('utf-8', errors='backslashreplace'), end='', flush=True)
        if err:
            print(err.decode('utf-8', errors='backslashreplace'), end='', flush=True)
        # The unmodified suite makes its own legacy locales. Require no
        # diagnostics, but do not invent individual localedef exit statuses.
        assert not err, ('original suite stderr', err)
        lines = out.splitlines()
        assert lines.count(b'39 passed') == 1 and lines.count(b'0 failed') == 1
        assert sum(line.startswith(b'passed: ') for line in lines) == 39
        assert not any(line.startswith(b'FAILED: ') for line in lines)
        # Do not reuse/delete a stale unrelated directory. The original suite
        # owns and removes its /tmp/test-par-$$ directory; leftovers fail QA.
        assert not set(Path('/tmp').glob('test-par-*'))
        out, err = command([binary, 'version'], env, work, payload=b'')
        assert out == b'par 1.53.0\n' and not err
        out, err = command([binary, 'help'], env, work, payload=b'')
        assert b'help' in out and b'version' in out and not err
        out, err = command([binary, 'xyz-invalid'], env, work, payload=b'', status=1)
        assert out.startswith(b'par error:\n') and not err
        payload = b'one two three four five\n'
        out, err = command([binary, 'w12'], env, work, payload=payload)
        assert not err and out.endswith(b'\n')
        assert b' '.join(out.split()) == b' '.join(payload.split())
        assert all(len(line) <= 12 for line in out.splitlines())
        print('PAR_QA_COMPLETE ' + json.dumps(dict(original_passed=39,
              original_failed=0, legacy_locales_verified=2,
              fixture_bytes_unchanged=True, default_make_test=args.make_default_test,
              binary=binary, suite_sha256=TEST_SHA)), flush=True)

if __name__ == '__main__':
    main()
PAR_QA

%build
make %{?_smp_mflags} -f protoMakefile

%check
python3 downstream-qa.py --binary "$PWD/par" --suite "$PWD/test-par" --make-default-test

%install
# No upstream install target exists; only the built binary/manual are placed.
install -Dpm0755 par %{buildroot}%{_bindir}/par
install -Dpm0644 par.1 %{buildroot}%{_mandir}/man1/par.1
install -Dpm0644 test-par %{buildroot}%{_libexecdir}/par-tests/test-par
install -Dpm0644 downstream-qa.py %{buildroot}%{_libexecdir}/par-tests/installed-check.py
python3 downstream-qa.py --binary %{buildroot}%{_bindir}/par --suite %{buildroot}%{_libexecdir}/par-tests/test-par

%files
%license par.doc
%doc par.doc releasenotes
%{_bindir}/par
%{_mandir}/man1/par.1*

%files tests
%license par.doc
%dir %{_libexecdir}/par-tests
%{_libexecdir}/par-tests/test-par
%{_libexecdir}/par-tests/installed-check.py

%changelog
* Wed Oct 21 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.53.0-1
- Preserve default flags and all 39 original cases from the fixed official commit
- Use complete original MIT-alternative notices and target-only legacy locale checks
