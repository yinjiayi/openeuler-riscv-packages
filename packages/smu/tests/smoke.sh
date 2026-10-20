#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
export LC_ALL=C
rpm -q -- smu smu-tests
test -x /usr/bin/smu
python3 -I -B /usr/libexec/smu-tests/run.py /usr/bin/smu /usr/share/smu/testdata
python3 -I -B - <<'SMU_INSTALLED'
import gzip
import hashlib
from pathlib import Path
for package in ('smu', 'smu-tests'):
    license_path = Path('/usr/share/licenses') / package / 'LICENSE'
    assert hashlib.sha256(license_path.read_bytes()).hexdigest() == '62d12c38a15f5de184bc3d9ab7070d27a019bb77b702788ba25573fdf97498df'
assert hashlib.sha256(Path('/usr/share/doc/smu/documentation').read_bytes()).hexdigest() == 'f8fee9f479e24027e2e387e3142eb94af050c088d16f5caa7c15a30128863a51'
paths = [p for p in (Path('/usr/share/man/man1/smu.1'), Path('/usr/share/man/man1/smu.1.gz')) if p.exists()]
assert len(paths) == 1
data = paths[0].read_bytes()
if paths[0].suffix == '.gz':
    data = gzip.decompress(data)
assert hashlib.sha256(data).hexdigest() == '9d38e714469e1fed371ef60cfdf05f46424f965dfb80ac24eb1328c6b145a202'
SMU_INSTALLED
