#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-pathlib-abc
cd /tmp
python3 -I - <<'PY'
import importlib.metadata
import pathlib
import posixpath
import tempfile
from pathlib_abc import JoinablePath, PathParser, ReadablePath, WritablePath, vfspath, vfsopen

assert importlib.metadata.version('pathlib-abc') == '0.5.2'
assert isinstance(posixpath, PathParser)
assert issubclass(ReadablePath, JoinablePath)
assert issubclass(WritablePath, JoinablePath)

class VirtualPath(JoinablePath):
    parser = posixpath

    def __init__(self, *segments):
        self.value = posixpath.join(*segments) if segments else ''

    def __vfspath__(self):
        return self.value

    def with_segments(self, *segments):
        return type(self)(*segments)

    def __eq__(self, other):
        return isinstance(other, VirtualPath) and self.value == other.value

p = VirtualPath('/archive', 'reports', 'item.tar.gz')
assert vfspath(p) == '/archive/reports/item.tar.gz'
assert p.parts == ('/', 'archive', 'reports', 'item.tar.gz')
assert p.anchor == '/' and p.name == 'item.tar.gz' and p.stem == 'item.tar'
assert p.suffix == '.gz' and p.suffixes == ['.tar', '.gz']
assert vfspath(p.parent) == '/archive/reports'
assert vfspath(p.with_suffix('.txt')) == '/archive/reports/item.tar.txt'
assert vfspath(p.with_name('other.txt')) == '/archive/reports/other.txt'
assert vfspath(p.relative_to(VirtualPath('/archive'))) == 'reports/item.tar.gz'
assert p.is_relative_to(VirtualPath('/archive'))
assert p.full_match('/archive/**/*.tar.gz')
assert not p.full_match('/elsewhere/**')
with tempfile.TemporaryDirectory(prefix='pathlib-abc-smoke-') as tmp:
    target = pathlib.Path(tmp) / 'roundtrip.txt'
    with vfsopen(target, 'w', encoding='utf-8') as stream:
        stream.write('installed pathlib-abc\n')
    with vfsopen(target, 'r', encoding='utf-8') as stream:
        assert stream.read() == 'installed pathlib-abc\n'
print('installed pathlib-abc version, ABCs, path operations and vfsopen passed')
PY
