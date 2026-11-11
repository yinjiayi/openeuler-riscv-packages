#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
export LC_ALL=C
rpm -q -- sprop sprop-tests
test -x /usr/bin/sprop
python3 -I -B /usr/libexec/sprop/qa.py /usr/bin/sprop
python3 -I -B - <<'SPROP_INSTALLED'
import gzip
import hashlib
from pathlib import Path
for name in ('sprop', 'sprop-tests'):
    assert hashlib.sha256((Path('/usr/share/licenses') / name / 'LICENSE').read_bytes()).hexdigest() == '8f1edfb4699060e27ea95e717a4d7de46bc9c1f4cbf47a39d6f6e4402bae07dc'
assert hashlib.sha256(Path('/usr/share/doc/sprop/README').read_bytes()).hexdigest() == '790e4ba2f7f3b990aa286a1d461311d565f33acce623a895cade81af947ad35f'
paths = [p for p in (Path('/usr/share/man/man1/sprop.1'), Path('/usr/share/man/man1/sprop.1.gz')) if p.exists()]
assert len(paths) == 1
data = paths[0].read_bytes()
if paths[0].suffix == '.gz':
    data = gzip.decompress(data)
assert data == b'.TH SPROP 1 sprop\\-0.1\n.SH NAME\nsprop \\- simple X property utility\n.SH SYNOPSIS\n.B sprop\n.I xid atom\n.RI [ value ]\n[\\-v]\n.SH DESCRIPTION\n.SS Overview\nThe\n.I sprop\nutility prints the value of the property\n.I atom\nof the window with the given\n.IR xid ,\nor alternatively sets it to\n.I value\nif given. sprop can only interact with atoms which are strings.\n.SS Options\n.TP\n.B \\-v\nprints version information to standard output, then exits.\n'
SPROP_INSTALLED
