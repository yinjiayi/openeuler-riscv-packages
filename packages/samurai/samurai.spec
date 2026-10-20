# SPDX-License-Identifier: Apache-2.0
Name:           samurai
Version:        1.3
Release:        1%{?dist}
Summary:        Ninja-compatible build tool written in C99
License:        ISC AND Apache-2.0 AND MIT
URL:            https://github.com/michaelforney/samurai
Source0:        samurai-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  python3
BuildRequires:  binutils
Requires:       bash

%description
Samurai implements the Ninja build language through version 1.9.0, except MSVC
dependency handling, using a portable C99/POSIX implementation.

%package tests
Summary:        Offline functional checks and retained source for Samurai
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash

%description tests
Authored downstream functional checks and the exact unchanged official source
archive. Upstream has no test/check target or test suite in the captured release.

%prep
%autosetup -n samurai-4288e71812493cb21b54ef23642a13214f44885f -p1
cat > downstream-qa.py <<'SAMURAI_QA'
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 yinjiayi. Licensed under the Apache License, Version 2.0.
"""Authored offline functional checks, not upstream/native/performance tests."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

root = Path(sys.argv[1]).resolve(strict=True)
binary = Path(sys.argv[2]).resolve(strict=True) if len(sys.argv) == 3 else root / 'usr/bin/samu'
assert binary.is_file() and os.access(binary, os.X_OK)
elf = binary.read_bytes()[:20]
assert elf[:6] == b'\x7fELF\x02\x01' and int.from_bytes(elf[18:20], 'little') == 243
assert Path(sys.executable).resolve().is_file() and sys.flags.isolated and sys.flags.dont_write_bytecode
archive = root / 'usr/share/samurai/qa/samurai-1.3.tar.gz'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == 'c1e5052f438034bd2eb3cc6cba020952110c4b3411964c7b06267b05d04a64e3'
with tarfile.open(archive, 'r:gz') as source:
    members = [member for member in source.getmembers() if member.isfile()]
    original = {member.name.split('/', 1)[1]: source.extractfile(member).read() for member in members}
assert len(original) == 37
for package in ('samurai', 'samurai-tests'):
    assert (root / 'usr/share/licenses' / package / 'LICENSE').read_bytes() == original['LICENSE']
assert (root / 'usr/share/doc/samurai/README.md').read_bytes() == original['README.md']
manual = root / 'usr/share/man/man1/samu.1'
assert (manual.read_bytes() if manual.exists() else gzip.decompress(manual.with_suffix('.1.gz').read_bytes())) == original['samu.1']
checks = ['fixed-source-full-notices-doc-and-manual']
with tempfile.TemporaryDirectory(prefix='samurai-qa-') as temporary:
    base = Path(temporary)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': str(base)}
    def run(directory, args=(), code=0, extra=None):
        current = dict(env)
        if extra:
            current.update(extra)
        result = subprocess.run([str(binary), *args], cwd=directory, env=current,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        assert result.returncode == code, (args, result.returncode, result.stdout, result.stderr)
        return result
    def scenario(name, manifest):
        directory = base / name
        directory.mkdir()
        (directory / 'build.ninja').write_text(manifest)
        return directory
    def content(directory, name):
        return (directory / name).read_bytes()
    assert run(base, ['--version']).stdout == b'1.9.0\n'
    checks.append('supported-ninja-language-version')
    common = 'rule emit\n  command = printf alpha > $out; printf c >> calls\n  description = EMIT $out\n'
    d = scenario('basic', common + 'build result: emit input\nbuild all: phony result\ndefault all\n')
    (d / 'input').write_text('input\n')
    run(d, ['-n'])
    assert not (d / 'result').exists() and not (d / 'calls').exists()
    run(d, ['-j', '2', '-v'])
    assert content(d, 'result') == b'alpha' and content(d, 'calls') == b'c'
    log = content(d, '.ninja_log')
    assert log.startswith(b'# ninja log v5\n')
    run(d)
    assert content(d, 'calls') == b'c' and content(d, '.ninja_log') == log
    # Force an ordering relation without sleeps or a timing assertion.
    old = (d / 'input').stat().st_mtime_ns - 2000000000
    os.utime(d / 'result', ns=(old, old))
    run(d, ['-d', 'explain'])
    assert content(d, 'calls') == b'cc'
    manifest = (d / 'build.ninja').read_text().replace('printf alpha', 'printf beta')
    (d / 'build.ninja').write_text(manifest)
    run(d)
    assert content(d, 'result') == b'beta' and content(d, 'calls') == b'ccc'
    checks.append('dryrun-default-phony-build-incremental-mtime-command-change')
    commands = run(d, ['-t', 'commands', 'result']).stdout
    assert b'printf beta' in commands
    query = run(d, ['-t', 'query', 'result']).stdout
    assert b'result:\n  input: emit\n    input\n' in query and b'    all\n' in query
    assert b'result: emit\n' in run(d, ['-t', 'targets', 'all']).stdout
    assert run(d, ['-t', 'targets', 'rule', 'emit']).stdout == b'result\n'
    assert b'all: phony' in run(d, ['-t', 'targets', 'depth', '2']).stdout
    graph = run(d, ['-t', 'graph', 'result']).stdout
    assert graph.startswith(b'digraph ninja {\n') and b'label="result"' in graph and b'label="input"' in graph
    database = json.loads(run(d, ['-t', 'compdb', 'emit']).stdout)
    assert len(database) == 1 and database[0]['file'] == 'input' and database[0]['output'] == 'result'
    assert database[0]['directory'] == str(d) and 'printf beta' in database[0]['command']
    run(d, ['-t', 'clean', 'result'])
    assert not (d / 'result').exists() and (d / 'input').exists()
    run(d)
    assert content(d, 'result') == b'beta'
    run(d, ['-t', 'clean', '-r', 'emit'])
    assert not (d / 'result').exists()
    checks.append('six-subtools-structured-compdb-and-clean-rebuild')
    run(base, ['-C', str(d), '-f', 'build.ninja', '-j', '1'], extra={'SAMUFLAGS': '-v -j 2'})
    assert content(d, 'result') == b'beta'
    checks.append('directory-manifest-and-environment-options')
    d = scenario('scope', 'value = root\ninclude shared.ninja\nsubninja child.ninja\nbuild outer: emit\ndefault outer inner\n')
    (d / 'shared.ninja').write_text('rule emit\n  command = printf $value > $out\n')
    (d / 'child.ninja').write_text('value = child\nbuild inner: emit\n')
    run(d)
    assert content(d, 'outer') == b'root' and content(d, 'inner') == b'child'
    checks.append('include-subninja-variable-scope')
    d = scenario('rsp', 'rule rsp\n  command = read value < $rspfile; printf "$$value" > $out\n  rspfile = args.rsp\n  rspfile_content = response\nbuild answer: rsp input\n')
    (d / 'input').write_text('input\n')
    run(d, ['-d', 'keeprsp'])
    assert content(d, 'answer') == b'response' and content(d, 'args.rsp') == b'response'
    run(d, ['-t', 'clean'])
    assert not (d / 'answer').exists() and not (d / 'args.rsp').exists()
    run(d)
    assert content(d, 'answer') == b'response' and not (d / 'args.rsp').exists()
    checks.append('response-file-retention-default-removal-and-clean')
    d = scenario('depfile', 'rule dep\n  command = printf object > $out; printf "obj: input header\\n" > obj.d; printf c >> calls\n  depfile = obj.d\n  deps = gcc\nbuild obj: dep input\n')
    (d / 'input').write_text('input\n')
    (d / 'header').write_text('header\n')
    run(d)
    assert content(d, 'calls') == b'c' and content(d, '.ninja_deps').startswith(b'# ninjadeps\n')
    run(d)
    assert content(d, 'calls') == b'c'
    old = (d / 'header').stat().st_mtime_ns - 2000000000
    os.utime(d / 'obj', ns=(old, old))
    run(d)
    assert content(d, 'calls') == b'cc'
    checks.append('gcc-depfile-log-and-header-rebuild')
    d = scenario('pool', 'pool serial\n  depth = 1\nrule emit\n  command = printf $out > $out\n  pool = serial\nbuild left: emit\nbuild right: emit || left\nbuild all: phony left right\ndefault all\n')
    run(d, ['-j', '2'])
    assert content(d, 'left') == b'left' and content(d, 'right') == b'right'
    checks.append('pool-and-order-only-dependencies')
    bad = [
        ('future', 'ninja_required_version = 99.0\n', 'newer than'),
        ('missing-rule', 'build out: undefined\n', 'undefined rule'),
        ('missing-input', common + 'build out: emit absent\n', 'file is missing'),
        ('duplicate', common + 'build out: emit\nbuild out: emit\n', 'multiple rules generate'),
        ('cycle', 'build one: phony two\nbuild two: phony one\ndefault one\n', 'dependency cycle'),
        ('bad-rsp', 'rule r\n  command = printf x\n  rspfile = args\n', 'rspfile_content'),
        ('command-failure', 'rule fail\n  command = exit 7\nbuild out: fail\n', 'subcommand failed')
    ]
    for name, manifest, message in bad:
        d = scenario(name, manifest)
        assert message.encode() in run(d, code=1).stderr
    d = scenario('unknown', common + 'build out: emit\n')
    assert b'unknown target' in run(d, ['absent'], 1).stderr
    assert b'invalid -j parameter' in run(d, ['-j', '-1'], 1).stderr
    assert b'unknown tool' in run(d, ['-t', 'absent'], 1).stderr
    assert b'invalid option in SAMUFLAGS' in run(d, code=1, extra={'SAMUFLAGS': '-n'}).stderr
    assert b'usage:' in run(d, ['--absent'], 2).stderr
    checks.append('twelve-invalid-input-command-and-option-boundaries')
print('SAMURAI_QA_OK ' + json.dumps(checks))
SAMURAI_QA

%build
# Upstream appends its original C99/warning flags and retains default -lrt.
%make_build CC=gcc CFLAGS='%{build_cflags}' LDFLAGS='%{build_ldflags}'

%install
%make_install CC=gcc CFLAGS='%{build_cflags}' LDFLAGS='%{build_ldflags}' PREFIX=%{_prefix} BINDIR=%{_bindir} MANDIR=%{_mandir}
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dm 0644 LICENSE %{buildroot}%{_licensedir}/%{name}-tests/LICENSE
install -Dm 0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -Dm 0644 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/qa/%{name}-%{version}.tar.gz
install -Dm 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/qa.py

%check
# No original test/check target exists. These are new downstream checks.
/usr/bin/python3 -I -B downstream-qa.py %{buildroot} "$PWD/samu"
/usr/bin/python3 -I -B downstream-qa.py %{buildroot}

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{_bindir}/samu
%{_mandir}/man1/samu.1*

%files tests
%license %{_licensedir}/%{name}-tests/LICENSE
%{_datadir}/%{name}/qa
%{_libexecdir}/%{name}-tests

%changelog
* Tue Oct 20 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.3-1
- Preserve the original C99/POSIX default build and complete upstream notices.
- Add offline built, staged and installed functional QA without an upstream-suite claim.
