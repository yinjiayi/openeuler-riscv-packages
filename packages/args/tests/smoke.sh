#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- args
python3 - <<'PY'
import hashlib,pathlib
root=pathlib.Path('/usr/share/licenses/args/source-notices')
rows=(root/'SHA256SUMS').read_text().splitlines();assert len(rows)==209
for line in rows:
    sha,name=line.split('  ',1);p=root/name;assert p.is_file() and not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==sha
PY
python3 /usr/share/args-tests/run-qa.py --prefix /usr
