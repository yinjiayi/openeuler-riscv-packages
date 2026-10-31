#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
export LC_ALL=C
rpm -q -- lemonbar lemonbar-tests
test -x /usr/bin/lemonbar
python3 -I -B /usr/libexec/lemonbar/qa.py /usr/bin/lemonbar
python3 -I -B - <<'LEMONBAR_INSTALLED'
import gzip
import hashlib
from pathlib import Path
for name in ('lemonbar', 'lemonbar-tests'):
    assert hashlib.sha256((Path('/usr/share/licenses') / name / 'LICENSE').read_bytes()).hexdigest() == '7a579731b29f6bd3bd34db18398689ab19df53969a407db862ca033ccf912133'
assert hashlib.sha256(Path('/usr/share/doc/lemonbar/README.pod').read_bytes()).hexdigest() == '56b612cf0beedd83ad4c1247a793a86d722cc4b2dd7e27c8e19a66c8ef56adbf'
pages = list(Path('/usr/share/man/man1').glob('lemonbar.1*'))
assert len(pages) == 1
data = gzip.decompress(pages[0].read_bytes()) if pages[0].suffix == '.gz' else pages[0].read_bytes()
assert b'lemonbar 1.4' in data and b'Featherweight lemon-scented bar' in data.replace(b'\\-', b'-')
LEMONBAR_INSTALLED
