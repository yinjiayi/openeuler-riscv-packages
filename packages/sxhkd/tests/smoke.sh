#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-2-Clause
set -euo pipefail
export LC_ALL=C
rpm -q -- sxhkd sxhkd-tests
test -x /usr/bin/sxhkd
python3 -I -B /usr/libexec/sxhkd-tests/qa.py /usr/bin/sxhkd
python3 -I -B - <<'SXHKD_INSTALLED'
import gzip
import hashlib
from pathlib import Path
for name in ('sxhkd', 'sxhkd-tests'):
    assert hashlib.sha256((Path('/usr/share/licenses') / name / 'LICENSE').read_bytes()).hexdigest() == 'b70a495eb48564c345d63e0ffea127e7e1e465ec8495e2383186fce0cafac804'
assert hashlib.sha256(Path('/usr/share/doc/sxhkd/README.md').read_bytes()).hexdigest() == '8db15c3036690e95fcb9315a7a2ba42a5e9f85ce906e47a56a5bc5fbe2353a05'
pages = list(Path('/usr/share/man/man1').glob('sxhkd.1*'))
assert len(pages) == 1
raw = pages[0].read_bytes()
data = gzip.decompress(raw) if pages[0].suffix == '.gz' else raw
assert hashlib.sha256(data).hexdigest() == 'a0246050901988396a5a27ba437848357ae331d28b6ec0b54d40f673c3b692b0'
examples = {'examples/background_shell/profile': '260893515516271017aa509f52d6aa3f0f07e35c2791c770bdb0e4788ee3d6fb', 'examples/background_shell/shell': 'ddcd7baa0cb55175804a27465381301f3b9964695ddff80589502b214c6edf7c', 'examples/background_shell/sxhkdrc': '2b185536e5b270ba6e44476c011e3da5ae5023a40ddb0a247e1d9eee52d597f1', 'examples/background_shell/xinitrc': '6117975018b8339b6d6647259165ec7699eccd4cd92ceec0e4deabae19c70ace', 'examples/notification/autostart': '845a271b8a30cf9f8b48bd75abce09a8d4aad51ec1936765dd9660e841f58f07', 'examples/notification/pam_environment': 'bafed8a2cc9e1118c468c57ad1709a9effecdcc74066d888405430a56ec1c164', 'examples/notification/sxhkd_notify': 'b66b759009791654463a01d380e0d60c5567dee1b1910cb75b43f110a2e9b96b', 'examples/notification/xinitrc': '5327608f591fca6fc1ebf12c3a6386f30f54d22030c273d5cc356ddfabfd9c61'}
root = Path('/usr/share/doc/sxhkd')
assert {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / 'examples').rglob('*') if p.is_file()} == examples
SXHKD_INSTALLED
