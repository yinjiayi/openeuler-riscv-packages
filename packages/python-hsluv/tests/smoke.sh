#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-hsluv
test_dir=$(mktemp -d)
trap 'rmdir "$test_dir"' EXIT
cd "$test_dir"
PYTHONNOUSERSITE=1 python3 - <<'PY'
import json
from pathlib import Path
import unittest
import hsluv

module = Path(hsluv.__file__).resolve()
assert str(module).startswith('/usr/lib/python3.11/site-packages/'), module
assert hsluv.__version__ == '5.0.4', hsluv.__version__
data = Path('/usr/share/python-hsluv')
with (data / 'tests/snapshot-rev4.json').open() as stream:
    assert len(json.load(stream)) == 4096, 'incomplete installed snapshot'
suite = unittest.defaultTestLoader.discover(str(data / 'tests'), top_level_dir=str(data))
assert suite.countTestCases() == 2, ('incomplete installed suite', suite.countTestCases())
result = unittest.TextTestRunner(verbosity=2).run(suite)
assert result.testsRun == 2 and result.wasSuccessful(), 'installed upstream suite failed'
assert not result.skipped, ('upstream tests skipped', result.skipped)
PY
