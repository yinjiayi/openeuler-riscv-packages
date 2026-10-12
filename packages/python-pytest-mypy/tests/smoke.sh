#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-pytest-mypy python3-filelock python3-mypy python3-pytest python3-packaging python3-pytest-cov python3-pytest-randomly python3-pytest-xdist python3-pexpect
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
python3 - <<'PY'
import ast
import hashlib
import importlib.metadata
from pathlib import Path
import subprocess
import pytest_mypy

assert importlib.metadata.version('pytest-mypy') == '1.0.1'
module = Path(pytest_mypy.__file__).resolve()
assert str(module).startswith('/usr/lib/') and module.parent.name == 'pytest_mypy'
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(module)], text=True) == 'python-pytest-mypy'
owned = Path('/usr/share/python-pytest-mypy/source')
expected = {
    '.github/workflows/publication.yml': 'f8f640cd08f2110b6c240fcf9543e1319f9df8557f21206115fffe5378e1dedb',
    '.github/workflows/validation.yml': '941a11e36a6eac2b023e5ecbda1bc8525fc60be71bdf68adeff217edf9cc1d82',
    '.gitignore': '0871634f97cc5f6890fd1de607559922d3f9ff52ac59784cc682549782168407',
    'CONTRIBUTING.rst': 'e936c4ea05d11d122d8f714cee195c24a633a1c295262522b608797db64f408e',
    'LICENSE': 'fa795384c183b89a4a9a5ba08fa67286eebeb61ad1adfff18d45aa6bc5d896ee',
    'README.rst': '6f1e5a91967bfc98f5fd691b5640e82745e9115aa774271a804cf8e8aa597f63',
    'changelog.md': '85a53a17e1af51df6a1f0f5f23c7a9e6f693cd8acc9425e183ca49e813d7e99f',
    'pyproject.toml': 'f1499c23c68d2d326422b2eba796acfe0fc4542a5c2c58279af43c39d0984deb',
    'src/pytest_mypy/__init__.py': '4a64a8335afa6a2a4d9f081563b0b2ec3d431d0c257cd37ffccb9d0094085ed5',
    'src/pytest_mypy/py.typed': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    'tests/conftest.py': '26b82604ca34a6a88222d1e63f2f0e72664c170589b214d03ebd867aa1228c8b',
    'tests/test_pytest_mypy.py': '62b258d494bb49d031816a551ab35e2a76d5e1aa06cd48c4633ab92be940ada6',
    'tox.ini': '4c2b6f29d26aaed73b3dfe998159334ebf2e986f80264dfc4c84d07b2625fbe4',
}
actual = {}
for path in sorted(owned.rglob('*')):
    assert not path.is_symlink()
    if path.is_file():
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(path)], text=True) == 'python-pytest-mypy'
        actual[str(path.relative_to(owned))] = hashlib.sha256(path.read_bytes()).hexdigest()
assert actual == expected
assert module.read_bytes() == (owned / 'src/pytest_mypy/__init__.py').read_bytes()
assert sum(isinstance(node, ast.FunctionDef) and node.name.startswith('test_') for node in ast.walk(ast.parse((owned / 'tests/test_pytest_mypy.py').read_bytes()))) == 29
ep = [e for e in importlib.metadata.distribution('pytest-mypy').entry_points if e.group == 'pytest11' and e.name == 'mypy']
assert len(ep) == 1 and ep[0].value == 'pytest_mypy'
print('Installed RPM-owned pytest-mypy 1.0.1, exact original 13 files and all 29 test functions verified; original skip/xfail retained')
PY
cp -R /usr/share/python-pytest-mypy/source/tests "$scratch/tests"
cp /usr/share/python-pytest-mypy/source/tox.ini "$scratch/tox.ini"
test ! -e "$scratch/pytest_mypy"
test ! -e "$scratch/src"
# Outer CLI verbosity only, matching source %check; nested pytester is unchanged.
# Retain whole original tests, xdist, branch coverage and existing deadlines.
# Non-exiting outer worker stack dump, not a test timeout or nested option.
# Flush complete failed reports from the outer controller before the deadline.
# The explicit plugin object is not exported to workers or pytester children.
python3 - -p no:mypy --cov pytest_mypy --cov-branch --cov-fail-under 100 --cov-report term-missing -n auto -vv -rA -o faulthandler_timeout=300 <<'OE_REPORT_PY'
import datetime
import json
import os
import sys
import pytest

class ImmediateFailureReporter:
    def __init__(self, stream):
        self.stream = stream

    def pytest_runtest_logreport(self, report):
        if not report.failed:
            return
        record = {
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "nodeid": report.nodeid,
            "when": report.when,
            "outcome": report.outcome,
            "duration": report.duration,
            "longreprtext": report.longreprtext,
            "sections": list(report.sections),
        }
        self.stream.write("OE_PYTEST_FAILURE_REPORT " + json.dumps(record, ensure_ascii=True) + "\n")
        self.stream.flush()

def main():
    descriptor = os.dup(2)
    os.set_inheritable(descriptor, False)
    with os.fdopen(descriptor, "w", encoding="utf-8", errors="backslashreplace") as stream:
        return int(pytest.main(sys.argv[1:], plugins=[ImmediateFailureReporter(stream)]))

if __name__ == "__main__":
    raise SystemExit(main())
OE_REPORT_PY
