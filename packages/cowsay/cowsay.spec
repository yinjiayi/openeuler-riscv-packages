# SPDX-License-Identifier: GPL-3.0-only
Name:           cowsay
Version:        3.8.4
Release:        1%{?dist}
Summary:        Configurable speaking and thinking cow
License:        GPL-3.0-only
URL:            https://cowsay.diamonds
Source0:        cowsay-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  coreutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  python3
BuildRequires:  bash
Requires:       perl
Requires:       coreutils
Requires:       perl(Cwd)
Requires:       perl(File::Basename)
Requires:       perl(File::Find)
Requires:       perl(Getopt::Std)
Requires:       perl(Text::Tabs)
Requires:       perl(Text::Wrap)

%description
Cowsay creates configurable speaking or thinking cow pictures from messages,
using the complete original51-cow collection and extensible cowpath registry.

%package tests
Summary:        Offline functional checks and retained complete Cowsay source
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash

%description tests
Authored downstream functional checks and the exact unchanged official source
archive. Upstream has a manual release checklist, not an automated test suite.

%prep
%autosetup -n cowsay-027c9268ac8571408e153214b9cf1a5e6fab0cfc -p1
cat > downstream-qa.py <<'COWSAY_QA'
# SPDX-License-Identifier: GPL-3.0-only
# Copyright 2026 yinjiayi. Distributed under GNU GPL version3, LICENSE.txt.
"""Authored target-only functional QA; not upstream/native/performance evidence."""
import gzip
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

root = Path(sys.argv[1]).resolve(strict=True)
assert sys.flags.isolated and sys.flags.dont_write_bytecode
archive = root / 'usr/share/cowsay/qa/cowsay-3.8.4.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == '74e78cd8a5d89c60ed4de1dc8211ccb395868234f5ffe2c6cab93088dc5010f2'
with tarfile.open(archive, 'r:gz') as source:
    original = {member.name.split('/', 1)[1]: source.extractfile(member).read()
                for member in source.getmembers() if member.isfile()}
assert len(original) == 73
binary = root / 'usr/bin/cowsay'
think = root / 'usr/bin/cowthink'
assert binary.read_bytes() == original['bin/cowsay'] and os.access(binary, os.X_OK)
assert think.is_symlink() and os.readlink(think) == 'cowsay'
for package in ('cowsay', 'cowsay-tests'):
    assert (root / 'usr/share/licenses' / package / 'LICENSE.txt').read_bytes() == original['LICENSE.txt']
for name in ('README.md', 'CHANGELOG.md', 'CONTRIBUTORS.md'):
    assert (root / 'usr/share/doc/cowsay' / name).read_bytes() == original[name]
assert (root / 'usr/share/doc/cowsay-tests/Release Checklist.md').read_bytes() == original['doc-project/Release Checklist.md']
manual = root / 'usr/share/man/man1/cowsay.1'
assert (manual.read_bytes() if manual.exists() else gzip.decompress(manual.with_suffix('.1.gz').read_bytes())) == original['man/man1/cowsay.1']
think_man = root / 'usr/share/man/man1/cowthink.1'
if not think_man.is_symlink():
    think_man = think_man.with_suffix('.1.gz')
assert think_man.is_symlink() and os.readlink(think_man) == ('cowsay.1.gz' if think_man.name.endswith('.gz') else 'cowsay.1')
cows = {Path(name).name[:-4]: data for name, data in original.items() if name.startswith('share/cowsay/cows/')}
assert len(cows) == 51
cowdir = root / 'usr/share/cowsay/cows'
assert sorted(path.name for path in cowdir.glob('*.cow')) == sorted(name + '.cow' for name in cows)
for name, data in cows.items():
    assert (cowdir / (name + '.cow')).read_bytes() == data
for name in ('usr/share/cowsay/site-cows', 'etc/cowsay/cowpath.d'):
    assert (root / name).is_dir()
checks = ['unchanged-source-full-notices-doc-manual-symlinks-and51cow-bytes']
with tempfile.TemporaryDirectory(prefix='cowsay-qa-') as temporary:
    base = Path(temporary)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(base),
           'COWPATH': str(cowdir), 'COWSAY_ONLY_COWPATH': '1'}
    def run(args=(), data=b'', program=binary, extra=None, success=True):
        current = dict(env)
        if extra:
            current.update(extra)
        result = subprocess.run([str(program), *args], input=data, cwd=base, env=current,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        assert (result.returncode == 0) == success, (args, result.returncode, result.stdout, result.stderr)
        return result
    # The actual target interpreter must load every original import.
    modules = ['Cwd','File::Basename','File::Find','Getopt::Std','Text::Tabs','Text::Wrap']
    loaded = subprocess.run(['/usr/bin/perl', *['-M' + name for name in modules], '-e', 'print "imports-ok\\n"'],
                            env=env, cwd=base, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
    assert loaded.returncode == 0 and loaded.stdout == b'imports-ok\n', loaded.stderr
    listed = run(['-l']).stdout.decode().splitlines()
    assert listed == sorted(cows)
    rendered = {}
    for cow in listed:
        out = run(['-f', cow, 'qa-message']).stdout
        assert b'< qa-message >' in out and len(out.splitlines()) > 3
        rendered[cow] = out
    assert run(['qa-message']).stdout == rendered['default']
    assert run(['-r', 'qa-message']).stdout in rendered.values()
    assert run(['-r', '-C', 'qa-message']).stdout in rendered.values()
    assert b'cowsay version 3.8.4' in run(['-h']).stdout
    checks.append('sixPerl-imports-parseable-list-all51cows-default-help-random')
    expected = (b' ____________\n< qa-message >\n ------------\n'
                b'        \\   ^__^\n         \\  (oo)\\_______\n'
                b'            (__)\\       )\\/\\\n                ||----w |\n                ||     ||\n')
    assert rendered['default'] == expected
    thought = run(['qa-message'], program=think).stdout
    assert b'( qa-message )' in thought and b'        o   ^__^' in thought
    for flag, eyes in [('-b', b'=='),('-d', b'xx'),('-g', b'$$'),('-p', b'@@'),
                       ('-s', b'**'),('-t', b'--'),('-w', b'OO'),('-y', b'..')]:
        assert b'(' + eyes + b')' in run([flag, 'qa-message']).stdout
    face = run(['-e', 'AB', '-T', 'CD', 'qa-message']).stdout
    assert b'(AB)' in face and b'CD ||----w |' in face
    assert run(data=b'qa-message\n').stdout == rendered['default']
    wrapped = run(['-W', '6', 'alpha beta gamma']).stdout
    assert wrapped.splitlines()[:5] == [b' _______', b'/ alpha \\', b'| beta  |', b'\\ gamma /', b' -------']
    assert all(word in wrapped for word in (b'alpha', b'beta', b'gamma'))
    assert b'alpha beta gamma' not in wrapped and len(wrapped.splitlines()) > len(expected.splitlines())
    assert b'< alpha   beta >' in run(['-n'], data=b'alpha   beta\n').stdout
    assert b'Usage:' in run(['-n', 'forbidden-argv'], success=False).stdout
    assert b'Could not find cowfile' in run(['-f', 'missing-cow', 'qa-message'], success=False).stderr
    checks.append('exact-default-think-eightfaces-customface-stdin-nowrap-wrap-negative-input')
    private = base / 'private'
    (private / 'bin').mkdir(parents=True)
    (private / 'share/cowsay/cows').mkdir(parents=True)
    (private / 'share/cowsay/site-cows').mkdir()
    (private / 'etc/cowsay/cowpath.d').mkdir(parents=True)
    shutil.copyfile(binary, private / 'bin/cowsay')
    (private / 'bin/cowsay').chmod(0o755)
    (private / 'bin/cowthink').symlink_to('cowsay')
    (private / 'share/cowsay/cows/default.cow').write_bytes(original['share/cowsay/cows/default.cow'])
    site = private / 'share/cowsay/site-cows'
    custom = base / 'custom'
    custom.mkdir()
    (custom / 'custom.cow').write_text('$the_cow = "CUSTOM-COW\\n";\n')
    (custom / 'reject.pm').write_text('die "must-not-execute";\n')
    (site / 'default.cow').write_text('$the_cow = "SITE-DEFAULT\\n";\n')
    (private / 'etc/cowsay/cowpath.d/extra.path').write_text(str(custom) + '\n')
    override = {'COWPATH': '', 'COWSAY_ONLY_COWPATH': '0'}
    assert run(['qa-message'], program=private / 'bin/cowsay', extra=override).stdout.endswith(b'SITE-DEFAULT\n')
    assert run(['-f', 'custom', 'qa-message'], program=private / 'bin/cowsay', extra=override).stdout.endswith(b'CUSTOM-COW\n')
    assert run(['-l'], program=private / 'bin/cowsay', extra=override).stdout == b'custom\ndefault\n'
    assert run(['-f', str(custom / 'custom.cow'), 'qa-message']).stdout.endswith(b'CUSTOM-COW\n')
    assert b'Could not find cowfile' in run(['qa-message'], extra={'COWPATH': str(custom)}, success=False).stderr
    rejected = run(['-f', str(custom / 'reject.pm'), 'qa-message'], success=False)
    assert b'.pm (Perl module) format cows are not implemented yet' in rejected.stderr
    assert b'must-not-execute' not in rejected.stderr
    checks.append('privateprefix-registry-siteprecedence-explicitpath-COWPATH-isolation-pm-rejection')
print('cowsay downstream functional QA: ' + '; '.join(checks))
COWSAY_QA

%build
make all

%install
make install prefix=%{_prefix} sysconfdir=%{_sysconfdir} DESTDIR=%{buildroot}
install -D -m0644 %{SOURCE0} %{buildroot}%{_datadir}/cowsay/qa/cowsay-%{version}.tar.gz
install -D -m0644 downstream-qa.py %{buildroot}%{_libexecdir}/cowsay-tests/qa.py
install -D -m0644 LICENSE.txt %{buildroot}%{_licensedir}/%{name}/LICENSE.txt
install -D -m0644 LICENSE.txt %{buildroot}%{_licensedir}/%{name}-tests/LICENSE.txt
install -D -m0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -D -m0644 CHANGELOG.md %{buildroot}%{_docdir}/%{name}/CHANGELOG.md
install -D -m0644 CONTRIBUTORS.md %{buildroot}%{_docdir}/%{name}/CONTRIBUTORS.md
install -D -m0644 'doc-project/Release Checklist.md' '%{buildroot}%{_docdir}/%{name}-tests/Release Checklist.md'

%check
/usr/bin/python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE.txt
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%doc %{_docdir}/%{name}/CONTRIBUTORS.md
%{_bindir}/cowsay
%{_bindir}/cowthink
%{_mandir}/man1/cowsay.1*
%{_mandir}/man1/cowthink.1*
%dir %{_datadir}/cowsay
%{_datadir}/cowsay/cows/
%dir %{_datadir}/cowsay/site-cows
%dir %{_sysconfdir}/cowsay
%dir %{_sysconfdir}/cowsay/cowpath.d

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE.txt
%doc "%{_docdir}/%{name}-tests/Release Checklist.md"
%{_libexecdir}/cowsay-tests/
%{_datadir}/cowsay/qa/

%changelog
* Wed Oct 21 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 3.8.4-1
- Preserve original default installation and add complete installed offline QA.
