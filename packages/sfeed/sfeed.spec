# SPDX-License-Identifier: ISC
Name:           sfeed
Version:        2.4
Release:        1%{?dist}
Summary:        RSS and Atom parser with feed formatting tools
License:        ISC
URL:            https://codemadness.org/sfeed-simple-feed-parser.html
Source0:        sfeed-2.4.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  binutils
BuildRequires:  ncurses-devel
BuildRequires:  coreutils
BuildRequires:  bash
BuildRequires:  python3
BuildRequires:  gawk
BuildRequires:  findutils
BuildRequires:  curl
BuildRequires:  glibc-common
BuildRequires:  less
BuildRequires:  lynx
BuildRequires:  tar
BuildRequires:  gzip
Requires:       bash
Requires:       coreutils
Requires:       gawk
Requires:       findutils
Requires:       curl
Requires:       glibc-common
Requires:       less
Requires:       lynx
Recommends:     xdg-utils

%description
Sfeed parses RSS and Atom XML to a documented tab-separated feed format.
The complete default toolset includes the curses interface, twelve other C
programs, four shell scripts and all nineteen manual pages. The default mono
theme, curses implementation and build flags are retained without patches.

%package tests
Summary:        Target-only functional checks for the complete Sfeed toolset
License:        ISC
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description tests
Authored parser, formatter, OPML, private loopback updater, read-state and curses
PTY checks. Upstream 2.4 ships no check target or regression fixtures. These
checks are not native-hardware, security or production-isolation certification.

%prep
%setup -q
cat > downstream-qa.py <<'SFEED_QA'
#!/usr/bin/python3
# SPDX-License-Identifier: ISC
# Copyright (c) 2026 yinjiayi
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
import argparse
import errno
import fcntl
import http.server
import json
import os
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import tempfile
import termios
import threading
import time
import xml.etree.ElementTree as ET

TOOLS = 'sfeed sfeed_atom sfeed_curses sfeed_frames sfeed_gopher sfeed_html sfeed_json sfeed_mbox sfeed_opml_import sfeed_plain sfeed_twtxt sfeed_web sfeed_xmlenc sfeed_content sfeed_markread sfeed_opml_export sfeed_update'.split()
RSS = b'''<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>QA feed</title><item><title>QA title</title><link>https://example.invalid/item</link><description>QA body</description><guid isPermaLink="false">qa-id</guid><pubDate>Thu, 02 Jan 2020 03:04:05 +0000</pubDate><author>QA author</author><category>QA category</category></item></channel></rss>'''

def kill_owned(process):
    if process.poll() is None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=15)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bindir', required=True)
    args = parser.parse_args()
    bindir = Path(args.bindir).resolve(strict=True)
    assert all((bindir / name).is_file() and os.access(bindir / name, os.X_OK) for name in TOOLS)
    with tempfile.TemporaryDirectory(prefix='sfeed-qa-') as directory:
        work = Path(directory)
        home = work / 'home'
        tmp = work / 'tmp'
        home.mkdir()
        tmp.mkdir()
        env = dict(PATH=str(bindir) + ':/usr/bin:/bin', HOME=str(home), TMPDIR=str(tmp), LC_ALL='C', LANG='C', TZ='UTC', TERM='xterm', PAGER='cat', NO_PROXY='127.0.0.1', no_proxy='127.0.0.1')
        evidence = []
        def run(name, payload=b'', extra=(), cwd=work, expected=0):
            process = subprocess.Popen([str(bindir / name), *map(str, extra)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, env=env, start_new_session=True)
            try:
                out, err = process.communicate(payload, timeout=30)
            except BaseException:
                kill_owned(process)
                raise
            assert process.returncode == expected, (name, process.returncode, out, err)
            evidence.append(dict(tool=name,exit=process.returncode,stdout_bytes=len(out),stderr_bytes=len(err)))
            return out, err
        tsv, err = run('sfeed', RSS)
        assert not err and len(tsv.splitlines()) == 1
        fields = tsv.rstrip(b'\n').split(b'\t')
        assert len(fields) == 9 and fields[0] == b'1577934245'
        assert fields[1:3] == [b'QA title', b'https://example.invalid/item']
        assert fields[3:7] == [b'QA body', b'html', b'qa-id', b'QA author'] and fields[8] == b'QA category', fields
        atom, err = run('sfeed_atom', tsv)
        assert not err
        root = ET.fromstring(atom)
        ns = '{http://www.w3.org/2005/Atom}'
        assert root.tag == ns + 'feed' and len(root.findall(ns + 'entry')) == 1
        assert root.find(ns + 'entry/' + ns + 'title').text == 'QA title'
        again, err = run('sfeed', atom)
        assert not err and again.split(b'\t')[1] == b'QA title'
        out, err = run('sfeed_json', tsv)
        data = json.loads(out)
        assert not err and len(data['items']) == 1 and data['items'][0]['title'] == 'QA title' and data['items'][0]['url'] == 'https://example.invalid/item'
        for name in ['sfeed_html', 'sfeed_plain', 'sfeed_twtxt', 'sfeed_mbox', 'sfeed_gopher']:
            out, err = run(name, tsv)
            assert not err and b'QA title' in out and b'example.invalid' in out, (name, out, err)
        out, err = run('sfeed_xmlenc', b'<?xml version="1.0" encoding="ISO-8859-1"?><rss/>')
        assert not err and out == b'iso-8859-1\n'
        out, err = run('sfeed_web', b'<html><head><link rel="alternate" type="application/rss+xml" href="/feed.xml"/></head></html>', extra=['https://example.invalid/base/'])
        assert not err and out == b'https://example.invalid/feed.xml\tapplication/rss+xml\n'
        feed = work / 'qa-feed'
        feed.write_bytes(tsv)
        frames = work / 'frames'
        frames.mkdir()
        run('sfeed_frames', extra=[feed], cwd=frames)
        assert all((frames / name).is_file() for name in ['index.html', 'items.html', 'menu.html'])
        assert b'QA title' in (frames / 'items.html').read_bytes()
        out, err = run('sfeed_content', tsv)
        assert not err and b'Title:     QA title' in out and b'QA body' in out
        urlfile = work / 'urls'
        url = b'https://example.invalid/item\n'
        run('sfeed_markread', url, ['read', urlfile])
        assert urlfile.read_bytes() == url
        run('sfeed_markread', url, ['unread', urlfile])
        assert urlfile.read_bytes() == b''
        config = work / 'sfeedrc'
        config.write_text("feeds() { feed 'QA feed' 'https://example.invalid/feed.xml'; }\n")
        out, err = run('sfeed_opml_export', extra=[config])
        assert not err and ET.fromstring(out).find('body/outline').attrib['xmlUrl'] == 'https://example.invalid/feed.xml'
        out, err = run('sfeed_opml_import', out)
        assert not err and b"feed 'QA feed' 'https://example.invalid/feed.xml'" in out
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != '/feed.xml':
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header('Content-Length', str(len(RSS)))
                self.end_headers()
                self.wfile.write(RSS)
            def log_message(self, *args):
                pass
        server = http.server.HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            config.write_text("feeds() { feed 'QA feed' 'http://127.0.0.1:" + str(server.server_port) + "/feed.xml'; }\n")
            for unused in range(2):
                out, err = run('sfeed_update', extra=[config])
                assert not err and b'OK' in out and b'FAIL' not in out
                assert (home / '.sfeed/feeds/QA feed').read_bytes() == tsv
            config.write_text("feeds() { feed 'bad' 'http://127.0.0.1:" + str(server.server_port) + "/missing'; }\n")
            out, err = run('sfeed_update', extra=[config], expected=1)
            assert b'FAIL (FETCH)' in err
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=10)
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 30, 110, 0, 0))
        process = subprocess.Popen([str(bindir / 'sfeed_curses'), str(feed)], stdin=slave, stdout=slave, stderr=slave, cwd=work, env=env, start_new_session=True)
        os.close(slave)
        output = bytearray()
        def until(predicate):
            deadline = time.monotonic() + 15
            while not predicate():
                assert time.monotonic() < deadline and process.poll() is None, bytes(output)
                if select.select([master], [], [], 0.1)[0]:
                    try:
                        chunk = os.read(master, 65536)
                    except OSError as exc:
                        if exc.errno != errno.EIO:
                            raise
                        chunk = b''
                    assert chunk, bytes(output)
                    output.extend(chunk)
                    assert len(output) < 2 * 1024 * 1024
        try:
            until(lambda: b'QA title' in output)
            os.write(master, b'ljkh\x0c3')
            os.write(master, b'q')
            deadline = time.monotonic() + 15
            while process.poll() is None:
                assert time.monotonic() < deadline, bytes(output)
                if select.select([master], [], [], 0.1)[0]:
                    try:
                        chunk = os.read(master, 65536)
                    except OSError as exc:
                        if exc.errno != errno.EIO:
                            raise
                        chunk = b''
                    output.extend(chunk)
                    assert len(output) < 2 * 1024 * 1024
            assert process.wait(timeout=15) == 0, bytes(output)
            evidence.append(dict(tool='sfeed_curses',exit=0,PTY=True,rendered_fixture=True,network_or_external_plumber_invoked=False))
        finally:
            kill_owned(process)
            os.close(master)
        assert not list(tmp.iterdir()), ('updater temporary files not cleaned', list(tmp.iterdir()))
        print(json.dumps(dict(sfeed_functional_checks='PASS',upstream_test_targets=[],upstream_tests_removed=0,default_C_tools=13,default_scripts=4,curses_default_mono=True,all_17_tools_exercised=True,external_feed_network=False,optional_xclip_xdg_open_not_exercised=True,checks=evidence), sort_keys=True), flush=True)
if __name__ == '__main__':
    main()
SFEED_QA

%build
%make_build

%check
python3 downstream-qa.py --bindir .

%install
%make_install PREFIX=%{_prefix} MANPREFIX=%{_mandir} DOCPREFIX=%{_docdir}/%{name}
install -Dpm0755 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/installed-check.py
python3 downstream-qa.py --bindir %{buildroot}%{_bindir}

%files
%license LICENSE strlcat.c strlcpy.c
%{_bindir}/sfeed
%{_bindir}/sfeed_*
%{_mandir}/man1/sfeed*.1*
%{_mandir}/man5/sfeed.5*
%{_mandir}/man5/sfeedrc.5*
%{_docdir}/%{name}

%files tests
%license LICENSE
%{_libexecdir}/%{name}-tests

%changelog
* Thu Oct 22 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 2.4-1
- Preserve the complete default build, curses UI, scripts and manuals.
- Add target-only full-toolset functional checks without source patches.
