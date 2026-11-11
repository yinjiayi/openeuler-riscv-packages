#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
export LC_ALL=C
rpm -q -- clipnotify clipnotify-tests
test -x /usr/bin/clipnotify
python3 -I -B /usr/libexec/clipnotify/qa.py /usr/bin/clipnotify
python3 -I -B - <<'CLIPNOTIFY_INSTALLED'
import hashlib
from pathlib import Path
for name in ('clipnotify', 'clipnotify-tests'):
    assert hashlib.sha256((Path('/usr/share/licenses') / name / 'LICENSE').read_bytes()).hexdigest() == 'd34c316184c3ff160b3fc554a444348be95eba0ec693f325e327e2b5236fc863'
assert hashlib.sha256(Path('/usr/share/doc/clipnotify/README.md').read_bytes()).hexdigest() == '5a232c2844cbd9d8afdfb52a0bf5c296b40f586099246e4972ca5ac4aa2ee267'
CLIPNOTIFY_INSTALLED
