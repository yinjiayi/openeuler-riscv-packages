#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- 9menu 9menu-tests
test -x /usr/bin/9menu
python3 /usr/libexec/9menu-tests/qa.py /usr/bin/9menu
python3 - <<'NINEMENU_INSTALLED'
from pathlib import Path
import gzip
import hashlib
for package in ('9menu', '9menu-tests'):
    notice = Path('/usr/share/licenses') / package / 'README'
    assert hashlib.sha256(notice.read_bytes()).hexdigest() == 'e866e54be9a8e484f34ad1f2114e9b2b59dc3ff68dc553acfd9e0c15e83a923b'
for filename, digest in (
    ('ChangeLog', '94f26ef9309f3a9329c0097b902d4613dd9d2f5c1973641c78567d51266a7ff9'),
    ('9menu.1', '6bbaa480c7054591958eb6bf4c8da4c7729b21fb663d3d90b34b0646344742e6')):
    assert hashlib.sha256((Path('/usr/share/doc/9menu') / filename).read_bytes()).hexdigest() == digest
manuals = list(Path('/usr/share/man/man1').glob('9menu.1*'))
assert len(manuals) == 1
data = gzip.decompress(manuals[0].read_bytes()) if manuals[0].suffix == '.gz' else manuals[0].read_bytes()
# Preserve default upstream CPP processing; compare strict original NAME semantics.
assert b'.SH NAME\n9menu \\- create a menu to run commands\n' in data
assert b'.TH 9MENU 1 "Feb 3 2023"' in data
assert b'.SH VERSION\nThis man page documents\n.I 9menu\nversion 1.11.\n' in data
NINEMENU_INSTALLED
