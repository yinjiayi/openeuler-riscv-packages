#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- slstatus slstatus-tests
test -x /usr/bin/slstatus
python3 -I -B /usr/libexec/slstatus-tests/qa.py /usr/bin/slstatus
python3 - <<'SLSTATUS_INSTALLED'
from pathlib import Path
import gzip
import hashlib
for package in ('slstatus', 'slstatus-tests'):
    assert hashlib.sha256((Path('/usr/share/licenses') / package / 'LICENSE').read_bytes()).hexdigest() == '44fc49b8c2c7c358a48027878889384399aa54fb36e67cb795bdae3b505cde23'
for name, digest in (('README', 'b244af6a5e96e5a74e3952a012ec8f5ee13a6d5c8a94a9638b8aeaf54df2512c'), ('config.def.h', '80b5c721ae797b236e2537bc96f027b3025972cb7243b4c77748d43b5b8ff697')):
    assert hashlib.sha256((Path('/usr/share/doc/slstatus') / name).read_bytes()).hexdigest() == digest
manuals = list(Path('/usr/share/man/man1').glob('slstatus.1*'))
assert len(manuals) == 1
data = gzip.decompress(manuals[0].read_bytes()) if manuals[0].suffix == '.gz' else manuals[0].read_bytes()
assert hashlib.sha256(data).hexdigest() == '188418832be4fc96b3c91d3daa8227720370f7ab9c9c1412196d76c820e910a5'
SLSTATUS_INSTALLED
