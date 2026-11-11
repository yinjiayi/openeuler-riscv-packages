#!/usr/bin/env bash
# SPDX-License-Identifier: ISC
set -euo pipefail
export LC_ALL=C
rpm -q -- scroll scroll-tests
test -x /usr/bin/scroll
python3 -I -B /usr/libexec/scroll-tests/qa.py /usr/bin/scroll
python3 -I -B - <<'SCROLL_INSTALLED'
import gzip
import hashlib
from pathlib import Path
for name in ('scroll', 'scroll-tests'):
    assert hashlib.sha256((Path('/usr/share/licenses') / name / 'LICENSE').read_bytes()).hexdigest() == '52f5f340941b3f63fc16882f3e17a9aa28751f7aedaf90f88922d14654b00e62'
for name, expected in {'README': 'db2cf29acbeeb3c64eb312b526bd9ca6bd15f3f2afe8d5fe17a314caf55d6094', 'TODO': 'fec75a6b12fb36ad2347a285b878492c58cda6d8b937ceb31e53ea71a5d3d9c0'}.items():
    assert hashlib.sha256((Path('/usr/share/doc/scroll') / name).read_bytes()).hexdigest() == expected
pages = list(Path('/usr/share/man/man1').glob('scroll.1*'))
assert len(pages) == 1
raw = pages[0].read_bytes()
data = gzip.decompress(raw) if pages[0].suffix == '.gz' else raw
assert hashlib.sha256(data).hexdigest() == '25a2fa843a97c455a894b5c45b9b05d23757467c1045455f0b4b811d4c65ad08'
SCROLL_INSTALLED
