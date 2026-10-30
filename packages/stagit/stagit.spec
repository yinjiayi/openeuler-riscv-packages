# SPDX-License-Identifier: MIT AND ISC
Name:           stagit
Version:        1.3
Release:        1%{?dist}
Summary:        Static HTML pages for Git repositories
License:        MIT AND ISC
URL:            https://codemadness.org/stagit.html
Source0:        stagit-1.3.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  libgit2-devel
BuildRequires:  python3
BuildRequires:  git
BuildRequires:  bash

%description
Stagit generates static HTML, Atom feeds, commit diffs, file and reference pages
for a Git repository. Stagit-index generates a repository index. The complete
default build, two manuals, style, images and both example scripts are retained.

%package tests
Summary:        Target-only functional checks for Stagit
License:        MIT AND ISC
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       git

%description tests
Private Git-fixture checks for both tools, escaping, text and binary files,
commit and reference pages, Atom feeds, cache and log limits. The full original
source is retained. Upstream ships no check target or regression suite.

%prep
%setup -q
cat > downstream-qa.py <<'STAGIT_QA'
#!/usr/bin/python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import xml.etree.ElementTree as ET

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bindir', required=True)
    args = parser.parse_args()
    bindir = Path(args.bindir).resolve(strict=True)
    assert all((bindir / n).is_file() and os.access(bindir / n, os.X_OK) for n in ('stagit', 'stagit-index'))
    with tempfile.TemporaryDirectory(prefix='stagit-qa-') as directory:
        work = Path(directory)
        home = work / 'home'
        home.mkdir()
        env = dict(PATH='/usr/bin:/bin', HOME=str(home), LC_ALL='C', LANG='C', TZ='UTC', GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', GIT_AUTHOR_DATE='2020-01-02T03:04:05+0000', GIT_COMMITTER_DATE='2020-01-02T03:04:05+0000')
        evidence = []
        def run(argv, cwd=work, expected=0):
            process = subprocess.Popen([str(x) for x in argv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, cwd=cwd, env=env, start_new_session=True)
            try:
                out, err = process.communicate(timeout=30)
            except BaseException:
                if process.poll() is None:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                process.wait(timeout=10)
                raise
            assert len(out) + len(err) < 2 * 1024 * 1024
            assert process.returncode == expected, (argv, process.returncode, out, err)
            evidence.append(dict(command=[str(x) for x in argv], exit=process.returncode))
            return out, err
        repo = work / 'fixture.git'
        repo.mkdir()
        def git(*args):
            return run(['/usr/bin/git', '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false', *args], cwd=repo)[0]
        git('init', '-q', '-b', 'main')
        git('config', 'user.name', 'QA Author')
        git('config', 'user.email', 'qa@example.invalid')
        (repo / 'README').write_text('QA README <tag> & text\n')
        (repo / 'LICENSE').write_text('QA fixture license\n')
        (repo / 'text.txt').write_text('first <tag> & text\n')
        (repo / 'binary.bin').write_bytes(b'\x00\x01\xff\x02')
        git('add', '.')
        git('commit', '-q', '-m', 'QA first <commit> & message')
        first = git('rev-parse', 'HEAD').decode().strip()
        git('tag', 'qa-tag')
        (repo / 'text.txt').write_text('second <tag> & text\n')
        git('add', 'text.txt')
        git('commit', '-q', '-m', 'QA second commit')
        second = git('rev-parse', 'HEAD').decode().strip()
        (repo / '.git/description').write_text('QA description <tag> & value\n')
        (repo / '.git/owner').write_text('QA owner <tag> & value\n')
        (repo / '.git/url').write_text('https://example.invalid/fixture.git\n')
        output = work / 'full'
        output.mkdir()
        run([bindir / 'stagit', '-u', 'https://example.invalid/project/', repo], cwd=output)
        required = ['log.html', 'files.html', 'refs.html', 'atom.xml', 'tags.xml', 'file/README.html', 'file/LICENSE.html', 'file/text.txt.html', 'file/binary.bin.html', 'commit/' + first + '.html', 'commit/' + second + '.html']
        assert all((output / n).is_file() for n in required)
        assert b'&lt;tag&gt; &amp; text' in (output / 'file/text.txt.html').read_bytes()
        assert b'Binary file.' in (output / 'file/binary.bin.html').read_bytes()
        log = (output / 'log.html').read_bytes()
        assert b'QA first &lt;commit&gt; &amp; message' in log and b'QA second commit' in log
        assert b'file/README.html' in log and b'file/LICENSE.html' in log
        assert b'qa-tag' in (output / 'refs.html').read_bytes() and b'main' in (output / 'refs.html').read_bytes()
        atom = ET.parse(output / 'atom.xml').getroot()
        ns = '{http://www.w3.org/2005/Atom}'
        assert atom.tag == ns + 'feed' and len(atom.findall(ns + 'entry')) == 2
        assert all(x.attrib['href'].startswith('https://example.invalid/project/') for x in atom.findall(ns + 'entry/' + ns + 'link'))
        assert len(ET.parse(output / 'tags.xml').getroot().findall(ns + 'entry')) == 1
        index, err = run([bindir / 'stagit-index', repo])
        assert not err and b'fixture/log.html' in index and b'QA description &lt;tag&gt; &amp; value' in index and b'QA owner &lt;tag&gt; &amp; value' in index
        limited = work / 'limited'
        limited.mkdir()
        run([bindir / 'stagit', '-l', '1', repo], cwd=limited)
        limited_log = (limited / 'log.html').read_bytes()
        assert b'QA second commit' in limited_log and b'QA first &lt;commit&gt;' not in limited_log
        cached = work / 'cached'
        cached.mkdir()
        cache = cached / 'history.cache'
        run([bindir / 'stagit', '-c', cache, repo], cwd=cached)
        original = (cached / 'log.html').read_bytes()
        assert cache.read_text().splitlines()[0] == second
        run([bindir / 'stagit', '-c', cache, repo], cwd=cached)
        assert (cached / 'log.html').read_bytes() == original
        run([bindir / 'stagit', '-c', cache, '-l', '1', repo], cwd=cached, expected=1)
        run([bindir / 'stagit', work / 'missing-repository'], expected=1)
        run([bindir / 'stagit-index', work / 'missing-repository'], expected=1)
        print('STAGIT_TARGET_QA ' + json.dumps(dict(tools=2, fixture_commits=2, checks=evidence), sort_keys=True))

if __name__ == '__main__':
    main()
STAGIT_QA

%build
%make_build CC="%{__cc}" CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" LIBGIT_INC="-I%{_includedir}" LIBGIT_LIB="-L%{_libdir} -lgit2"

%install
%make_install PREFIX="%{_prefix}" MANPREFIX="%{_mandir}" DOCPREFIX="%{_docdir}/%{name}"
install -d %{buildroot}%{_libexecdir}/%{name}-tests
install -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/installed-check.py
install -m 0644 %{SOURCE0} %{buildroot}%{_libexecdir}/%{name}-tests/stagit-1.3.tar.gz

%check
python3 downstream-qa.py --bindir "$PWD"
python3 downstream-qa.py --bindir "%{buildroot}%{_bindir}"

%files
%license LICENSE reallocarray.c strlcat.c strlcpy.c
%{_bindir}/stagit
%{_bindir}/stagit-index
%{_mandir}/man1/stagit.1*
%{_mandir}/man1/stagit-index.1*
%{_docdir}/%{name}

%files tests
%license LICENSE reallocarray.c strlcat.c strlcpy.c
%{_libexecdir}/%{name}-tests

%changelog
* Thu Oct 22 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.3-1
- Preserve default tools, manuals, examples and MIT/ISC notices; add target-only QA.
