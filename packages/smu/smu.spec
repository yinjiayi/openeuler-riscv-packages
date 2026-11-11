# SPDX-License-Identifier: MIT
Name:           smu
Version:        1.5
Release:        1%{?dist}
Summary:        Small simple-markup to HTML converter
License:        MIT
URL:            https://github.com/Gottox/smu
Source0:        smu-1.5.tar.gz
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  sed
BuildRequires:  python3

%description
A small command-line interpreter for the upstream simple-markup dialect. It
converts stdin or an input file to HTML. The default HTML passthrough behavior
is retained; this program is not an HTML sanitizer.

%package tests
Summary:        Mandatory offline CLI and original-fixture checks for smu
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       bash

%description tests
The unchanged original documentation and testdoc plus downstream exact-output,
CLI, stdin/file, escaping and allocation-growth checks. No original upstream
test target exists, and both original fixtures are always exercised in full.

%prep
%autosetup -n smu-67be1bfcb8643531ce7063423a7e45a2225439b8 -p1
cat > downstream-qa.py <<'SMU_QA'
# SPDX-License-Identifier: MIT
# Copyright 2026 yinjiayi. Distributed under the MIT license.
# Authored offline fixtures; the upstream program is executed only in target CI.
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

binary = str(Path(sys.argv[1]).resolve())
fixtures = Path(sys.argv[2]).resolve()
assert len(sys.argv) == 3 and os.access(binary, os.X_OK)
os.environ['LC_ALL'] = 'C'

def invoke(data=b'', args=(), cwd=None, status=0):
    result = subprocess.run([binary, *args], input=data, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=cwd, timeout=20, check=False)
    assert result.returncode == status, (args, result.returncode, result.stderr)
    if status == 0:
        assert not result.stderr, (args, result.stderr)
    return result

cases = [
    (b'', b''),
    (b'hello\n', b'<p>hello</p>\n'),
    (b'a *b* **c** `d`.\n', b'<p>a <em>b</em> <strong>c</strong> <code>d</code>.</p>\n'),
    (b'\\*lit\\* \\_x\\_\n', b'<p>*lit* _x_</p>\n'),
    (b'Title\n=====\n', b'<h1>Title</h1>\n'),
    (b'# Title\n', b'<h1>Title</h1>\n'),
    (b'[go](https://example.invalid/)\n', b'<p><a href="https://example.invalid/">go</a></p>\n'),
    (b'![alt](image.png "T")\n', b'<p><img src="image.png" alt="alt" title="T" /></p>\n'),
    (b'* a\n* b\n', b'<ul>\n<li>a</li>\n<li>b</li>\n</ul>\n'),
    (b'1. a\n2. b\n', b'<ol>\n<li>a</li>\n<li>b</li>\n</ol>\n'),
    (b'\t<>&"\n', b'<pre><code>&lt;&gt;&amp;&quot;\n</code></pre>\n'),
    (b'<b>X</b>\n', b'<p><b>X</b>\n</p>\n'),
]
for data, expected in cases:
    assert invoke(data).stdout == expected, (data, invoke(data).stdout, expected)
assert invoke(b'<tag>&"\n', ('-n',)).stdout == b'<p>&lt;tag&gt;&amp;&quot;</p>\n'
assert invoke(b'*hello*\n', ('-n',)).stdout == b'<p><em>hello</em></p>\n'
assert invoke(args=('-v',), status=1).stderr == b'simple markup 1.5 (C) Enno Boland\n'
for option in ('-h', '-not-an-option'):
    r = invoke(args=(option,), status=1)
    assert not r.stdout
    assert r.stderr == ('Usage ' + binary + ' [-n] [file]\n -n escape html strictly\n').encode()

with tempfile.TemporaryDirectory(prefix='smu-qa-') as tmp:
    root = Path(tmp)
    data = b'hello\n'
    for filename, args in [('with space', (str(root / 'with space'),)),
                           ('-dash', ('--', '-dash'))]:
        (root / filename).write_bytes(data)
        assert invoke(args=args, cwd=root).stdout == b'<p>hello</p>\n'
    missing = str(root / 'absent')
    result = invoke(args=(missing,), status=1)
    assert not result.stdout and result.stderr == ('Cannot open file `' + missing + '`\n').encode()

# Original default fixtures, unchanged: verify fixed-source identities and run
# each complete file through both file and stdin entry points, also in -n mode.
fixture_hashes = {
    'documentation': 'f8fee9f479e24027e2e387e3142eb94af050c088d16f5caa7c15a30128863a51',
    'testdoc': 'f4b88f4278c0bb80e3d96ee5e1fe2c644650d8b53a7722dadba1ecd1e5fcb8ad',
}
for name, digest in fixture_hashes.items():
    path = fixtures / name
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, name
    for args in ((), ('-n',)):
        stdin = invoke(data, args).stdout
        file = invoke(args=(*args, str(path))).stdout
        assert stdin == file and len(file) > len(data), (name, args)
        for token in (b'<h1>', b'<h2>', b'<em>', b'<strong>', b'<code>',
                      b'<ul>', b'<pre><code>', b'<a href='):
            assert token in file, (name, args, token)
    if name == 'testdoc':
        default = invoke(data).stdout
        for token in (b'<ol>', b'<blockquote>', b'<img src=', b'title="screenshot of st"', b'<center>'):
            assert token in default, token
        strict = invoke(data, ('-n',)).stdout
        assert b'&lt;center&gt;' in strict and b'<center>' not in strict

# Exercise allocation growth and UTF-8 byte preservation without fetching any
# literal links/images from the markup. This is not an HTML sanitizer claim.
large = (b'hello ' * 20000) + '\u6d4b\u8bd5'.encode() + b'\n'
assert invoke(large).stdout == b'<p>' + large[:-1] + b'</p>\n'
print('smu mandatory original-fixture and CLI QA passed')
SMU_QA

%build
# Preserve the original all target, strict warning/ANSI flags and library search
# path, replacing only optimization/debug/link settings with distribution flags.
%make_build CC=gcc PREFIX=%{_prefix} MANPREFIX=%{_mandir} \
    CFLAGS='%{optflags} -Wall -Werror -ansi -I. -I/usr/include -DVERSION=\"1.5\"' \
    LDFLAGS='%{?build_ldflags} -L/usr/lib'

%install
%make_install CC=gcc PREFIX=%{_prefix} MANPREFIX=%{_mandir} \
    CFLAGS='%{optflags} -Wall -Werror -ansi -I. -I/usr/include -DVERSION=\"1.5\"' \
    LDFLAGS='%{?build_ldflags} -L/usr/lib'
install -Dpm0644 downstream-qa.py %{buildroot}%{_libexecdir}/smu-tests/run.py
install -Dpm0644 documentation %{buildroot}%{_datadir}/smu/testdata/documentation
install -Dpm0644 testdoc %{buildroot}%{_datadir}/smu/testdata/testdoc

%check
python3 -I -B downstream-qa.py ./smu .
python3 -I -B downstream-qa.py %{buildroot}%{_bindir}/smu %{buildroot}%{_datadir}/smu/testdata

%files
%license LICENSE
%doc documentation
%{_bindir}/smu
%{_mandir}/man1/smu.1*

%files tests
%license LICENSE
%{_libexecdir}/smu-tests/
%{_datadir}/smu/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.5-1
- Import the official v1.5 commit without source patches or default test changes.
- Require unchanged upstream fixtures and offline CLI checks staged and installed.
