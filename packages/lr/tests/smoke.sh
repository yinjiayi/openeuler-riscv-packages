#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- lr lr-tests
test -x /usr/bin/lr
python3 -I -B /usr/libexec/lr-tests/qa.py /usr/bin/lr
zsh -n /usr/share/zsh/site-functions/_lr
python3 -I -B - <<'LR_INSTALLED'
from pathlib import Path
import gzip
import hashlib
for package in ('lr', 'lr-tests'):
    for name, digest in (('LICENSE', '9f491b1ba411ba03032e07c0d87794d0dd43b799ee4fd92c874dbf664796ebd4'), ('SOURCE-NOTICE', 'f534d8126d90ccde755ed7e625b94d77c0a15e7b020e9702f696fa7fff6144ee')):
        assert hashlib.sha256((Path('/usr/share/licenses') / package / name).read_bytes()).hexdigest() == digest
for name, digest in (('README.md', '57c199b63f49acd9755a7d2d156ed2e65b9cf1b8215462224d6a3d245363137e'), ('NEWS.md', '061d365d8578d258eb7eecbd41327ed09322ebc74c0c61bcb17e18d624f5b62d')):
    assert hashlib.sha256((Path('/usr/share/doc/lr') / name).read_bytes()).hexdigest() == digest
assert hashlib.sha256(Path('/usr/share/zsh/site-functions/_lr').read_bytes()).hexdigest() == '2eff74d2aae68c32d0818d88a1974f8af0e1ee24626dd4aa0018c8dac4632936'
manuals = list(Path('/usr/share/man/man1').glob('lr.1*'))
assert len(manuals) == 1 and manuals[0].name in ('lr.1', 'lr.1.gz')
raw = manuals[0].read_bytes()
decoded = gzip.decompress(raw) if manuals[0].name.endswith('.gz') else raw
assert hashlib.sha256(decoded).hexdigest() == '93c2ca357d227c9cac2399d1503b9a8e7f522438c42e0de0b6513443250185d5'
LR_INSTALLED
