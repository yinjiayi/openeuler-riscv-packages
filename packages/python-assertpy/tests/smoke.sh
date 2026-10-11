#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-assertpy
scratch=$(mktemp -d)
trap 'rmdir "$scratch" 2>/dev/null || true' EXIT
unset PYTHONPATH
cd "$scratch"
python3 - <<'PYTEST'
import importlib.metadata
import pathlib
import subprocess
import assertpy
import requests
import pytest_cov.plugin

assert importlib.metadata.version("assertpy") == "1.1"
assert assertpy.__version__ == "1.1"
assert callable(requests.structures.CaseInsensitiveDict)
path = pathlib.Path(assertpy.__file__).resolve()
assert path.is_absolute() and str(path).startswith("/usr/")
assert subprocess.check_output(["rpm", "-qf", "--qf", "%{NAME}", str(path)], text=True) == "python3-assertpy"
root = pathlib.Path("/usr/share/python-assertpy/tests")
files = sorted(root.rglob("*"))
assert len(list((root / "tests").glob("*.py"))) == 30
for source in files:
    assert not source.is_symlink()
    if source.is_file():
        assert subprocess.check_output(["rpm", "-qf", "--qf", "%{NAME}", str(source)], text=True) == "python3-assertpy"
PYTEST
cp -a /usr/share/python-assertpy/tests/tests /usr/share/python-assertpy/tests/setup.cfg /usr/share/python-assertpy/tests/.coveragerc .
test ! -e assertpy
PYTHONPATH=. python3 -m pytest -v --cov=assertpy --cov-report term-missing tests
# Keep isolated suite/coverage outputs for CI diagnostics.
