# SPDX-License-Identifier: GPL-2.0-or-later AND LicenseRef-Public-Domain
Name:           mktorrent
Version:        1.1
Release:        1%{?dist}
Summary:        Create BitTorrent metainfo files
License:        GPL-2.0-or-later AND LicenseRef-Public-Domain
URL:            https://github.com/pobrn/mktorrent
Source0:        mktorrent-1.1.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  python3
BuildRequires:  bash

%description
Mktorrent creates BitTorrent metainfo for a file or directory, including piece
hashes, tracker tiers, web seeds, comments and private tracker source strings.
The original six-object default build and bundled SHA-1 implementation remain.

%package tests
Summary:        Target-only functional checks for Mktorrent
License:        GPL-2.0-or-later AND LicenseRef-Public-Domain AND MIT
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description tests
Private deterministic single-file and directory fixtures verify bencoded fields,
complete SHA-1 piece strings, option handling and no-overwrite behavior. The full
original source archive, including optional SHA-1 self-tests, is retained.

%prep
%setup -q -n pobrn-mktorrent-b20ef69
cat > downstream-qa.py <<'MKTORRENT_QA'
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
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile

def decode(data):
    assert len(data) < 2 * 1024 * 1024
    def item(pos, depth):
        assert depth < 64 and pos < len(data)
        marker = data[pos:pos + 1]
        if marker == b'i':
            end = data.index(b'e', pos + 1)
            return int(data[pos + 1:end]), end + 1
        if marker in (b'l', b'd'):
            pos += 1
            values = []
            while data[pos:pos + 1] != b'e':
                value, pos = item(pos, depth + 1)
                values.append(value)
            if marker == b'l':
                return values, pos + 1
            assert len(values) % 2 == 0
            keys = values[::2]
            assert all(isinstance(k, bytes) for k in keys)
            assert keys == sorted(set(keys))
            return dict(zip(keys, values[1::2])), pos + 1
        end = data.index(b':', pos)
        length = int(data[pos:end])
        assert 0 <= length <= len(data) - end - 1
        return data[end + 1:end + 1 + length], end + 1 + length
    value, end = item(0, 0)
    assert end == len(data) and isinstance(value, dict)
    return value

def pieces(data, length):
    return b''.join(hashlib.sha1(data[n:n + length]).digest() for n in range(0, len(data), length))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary', required=True)
    args = parser.parse_args()
    binary = Path(args.binary).resolve(strict=True)
    assert binary.is_file() and os.access(binary, os.X_OK)
    with tempfile.TemporaryDirectory(prefix='mktorrent-qa-') as directory:
        work = Path(directory)
        env = dict(PATH='/usr/bin:/bin', HOME=str(work), LC_ALL='C', LANG='C', TZ='UTC')
        evidence = []
        def run(*args, expected=0):
            process = subprocess.Popen([str(binary), *map(str, args)], cwd=work, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
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
            assert process.returncode == expected, (args, process.returncode, out, err)
            evidence.append(dict(args=list(map(str, args)), exit=process.returncode))
            return out, err
        help_out, _ = run('-h')
        assert b'mktorrent 1.1' in help_out and b'Usage: mktorrent' in help_out
        single = bytes(range(256)) * 1200
        (work / 'single.bin').write_bytes(single)
        run('-d', '-a', 'https://tracker.invalid/announce', '-o', 'single.torrent', 'single.bin')
        torrent = decode((work / 'single.torrent').read_bytes())
        assert torrent[b'announce'] == b'https://tracker.invalid/announce'
        assert b'creation date' not in torrent and torrent[b'created by'] == b'mktorrent 1.1'
        assert torrent[b'info'] == {b'length': len(single), b'name': b'single.bin', b'piece length': 262144, b'pieces': pieces(single, 262144)}
        root = work / 'tree'
        (root / 'sub').mkdir(parents=True)
        fixture = [(('a.bin',), b'A' * 20000), (('sub', 'b.bin'), bytes(range(256)) * 160), (('z.bin',), b'Z' * 19000)]
        for path, content in fixture:
            root.joinpath(*path).write_bytes(content)
        run('-d', '-l', '15', '-n', 'fixture', '-p', '-s', 'QA-source', '-c', 'QA comment', '-a', 'https://first.invalid/a,https://second.invalid/a', '-a', 'https://backup.invalid/a', '-w', 'https://seed.invalid/a,https://seed.invalid/b', '-o', 'tree.torrent', 'tree')
        raw = (work / 'tree.torrent').read_bytes()
        multi = decode(raw)
        assert multi[b'announce-list'] == [[b'https://first.invalid/a', b'https://second.invalid/a'], [b'https://backup.invalid/a']]
        assert multi[b'url-list'] == [b'https://seed.invalid/a', b'https://seed.invalid/b']
        assert multi[b'comment'] == b'QA comment' and b'creation date' not in multi
        expected_files = [{b'length': len(content), b'path': [part.encode() for part in path]} for path, content in fixture]
        expected_pieces = pieces(b''.join(content for path, content in fixture), 32768)
        assert multi[b'info'] == {b'files': expected_files, b'name': b'fixture', b'piece length': 32768, b'pieces': expected_pieces, b'private': 1, b'source': b'QA-source'}
        run('-d', '-o', 'tree.torrent', 'single.bin', expected=1)
        assert (work / 'tree.torrent').read_bytes() == raw
        run('-l', '14', '-o', 'invalid.torrent', 'single.bin', expected=1)
        assert not (work / 'invalid.torrent').exists()
        run('missing-file', expected=1)
        print('MKTORRENT_TARGET_QA ' + json.dumps(dict(fixtures=2, default_piece_length=262144, cross_file_piece_length=32768, checks=evidence), sort_keys=True))

if __name__ == '__main__':
    main()
MKTORRENT_QA

%build
%make_build CC="%{__cc}" CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"

%install
%make_install PREFIX="%{_prefix}"
install -d %{buildroot}%{_libexecdir}/%{name}-tests
install -m 0644 downstream-qa.py %{buildroot}%{_libexecdir}/%{name}-tests/installed-check.py
install -m 0644 %{SOURCE0} %{buildroot}%{_libexecdir}/%{name}-tests/mktorrent-1.1.tar.gz

%check
# Upstream defines no check target; additionally run its unchanged opt-in vectors.
%{__cc} %{optflags} %{build_ldflags} -DSHA1_TEST sha1.c -o upstream-sha1-test
./upstream-sha1-test
python3 downstream-qa.py --binary "$PWD/mktorrent"
python3 downstream-qa.py --binary "%{buildroot}%{_bindir}/mktorrent"

%files
%license COPYING sha1.c sha1.h
%doc README
%{_bindir}/mktorrent

%files tests
%license COPYING sha1.c sha1.h
%{_libexecdir}/%{name}-tests

%changelog
* Thu Oct 22 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1-1
- Preserve all default sources and install behavior; add target-only metainfo QA.
