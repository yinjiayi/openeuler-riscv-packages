#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-hashids
test_dir=$(mktemp -d)
cd "$test_dir"
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
python3 - <<'PY'
from pathlib import Path
import hashids
from importlib.metadata import version
assert version('hashids') == '1.3.1'
assert str(Path(hashids.__file__).resolve()).startswith('/usr/lib/python3.11/site-packages/')
encoder = hashids.Hashids()
assert encoder.encode(1, 2, 3) == 'o2fXhV'
assert encoder.decode('o2fXhV') == (1, 2, 3)
PY
# No source tree on sys.path: rerun the entire installed original suite.
python3 -m pytest --junitxml=installed-results.xml /usr/share/python-hashids/test
python3 - <<'PY'
import xml.etree.ElementTree as ET
suites = ET.parse('installed-results.xml').getroot().findall('testsuite')
assert sum(int(s.attrib['tests']) for s in suites) == 60, 'incomplete installed suite'
for key in ('failures', 'errors', 'skipped'):
    assert sum(int(s.attrib[key]) for s in suites) == 0, key
PY
