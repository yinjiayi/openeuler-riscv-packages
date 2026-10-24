#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-stringcase
test_dir=$(mktemp -d)
cd "$test_dir"
export PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1
export COVERAGE_FILE="$test_dir/.coverage"
python3 - <<'PY'
from pathlib import Path
from importlib.metadata import version
import subprocess
import stringcase
assert version('stringcase') == '1.2.0'
assert str(Path(stringcase.__file__).resolve()).startswith('/usr/lib/python3.11/site-packages/')
owner = subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', stringcase.__file__], text=True)
assert owner == 'python3-stringcase', 'module not owned by the installed package'
assert stringcase.camelcase('foo_bar_baz') == 'fooBarBaz'
PY
# Copy only tests, never the source module: imports resolve to the installed RPM.
cp /usr/share/python-stringcase/test/stringcase_test.py .
python3 -m unittest -v stringcase_test.py
python3 -m coverage run -m unittest stringcase_test
python3 -m coverage html -d docs/report/coverage/
python3 - <<'PY'
import unittest
suite = unittest.defaultTestLoader.loadTestsFromName('stringcase_test')
assert suite.countTestCases() == 13, 'incomplete installed suite'
result = unittest.TextTestRunner(verbosity=2).run(suite)
assert result.testsRun == 13 and result.wasSuccessful() and not result.skipped
PY
