#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-pytimeparse
python3 -I - <<'PY'
import importlib.metadata
from pathlib import Path
import subprocess
import unittest
import pytimeparse
from pytimeparse import parse as timeparse

assert importlib.metadata.version('pytimeparse') == '1.1.9'
assert pytimeparse.__version__ == '1.1.9'
root = Path(pytimeparse.__file__).resolve().parent
for name in ('__init__.py', 'VERSION', 'timeparse.py', 'tests/testtimeparse.py', 'tests/testdayclock.py'):
    file = root / name
    assert file.is_file(), file
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}\n', str(file)], text=True).splitlines() == ['python3-pytimeparse'], file
assert timeparse('1w3d2h32m') == 873120
assert timeparse('-1.5m30s') == -120
assert timeparse('1-02:03:04') == 93784
assert timeparse('|5m') is None
# Complete installed source suite, including the original doctest test method;
# stdlib unittest runs these unchanged TestCase classes without runtime nose.
suite = unittest.defaultTestLoader.loadTestsFromNames([
    'pytimeparse.tests.testtimeparse', 'pytimeparse.tests.testdayclock',
])
result = unittest.TextTestRunner(verbosity=2).run(suite)
assert result.testsRun == 57, ('incomplete installed suite', result.testsRun)
assert result.wasSuccessful() and not result.skipped
print('pytimeparse 1.1.9 installed owner/version and complete suite passed')
PY
