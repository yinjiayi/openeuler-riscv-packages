#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C LANG=C
rpm -q pdfresurrect
qa=/usr/share/pdfresurrect-tests
(cd "$qa" && sha256sum -c SHA256SUMS)
python3 - <<'PY_NOTICES'
from pathlib import Path
import hashlib
roots=[p for p in Path('/usr/share/licenses').glob('pdfresurrect*') if (p/'source-notices/SHA256SUMS').is_file()]
assert len(roots)==1
root=roots[0];rows=(root/'source-notices/SHA256SUMS').read_text().splitlines();assert len(rows)==13
for line in rows:
    digest,name=line.split('  ',1);p=root/'source-notices'/name
    assert p.is_file() and not p.is_symlink() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
assert hashlib.sha256((root/'Apache-2.0.txt').read_bytes()).hexdigest()=='cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30'
assert hashlib.sha256(Path('/usr/share/pdfresurrect-tests/run-qa.py').read_bytes()).hexdigest()=='5358f476e15a3c51ccd4a2d261258dfcc5bb3ecbea25ad9f01338165d3859d75'
PY_NOTICES
python3 "$qa/run-qa.py" --program /usr/bin/pdfresurrect --required-program /usr/bin/pdfresurrect
