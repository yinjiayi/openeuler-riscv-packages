#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python3-expandvars
scratch=$(mktemp -d)
trap 'rmdir "$scratch" 2>/dev/null || true' EXIT
unset PYTHONPATH
cd "$scratch"
python3 - <<'PYTEST'
import hashlib
import importlib.metadata
import pathlib
import subprocess
import expandvars
import pytest_cov.plugin

assert importlib.metadata.version("expandvars") == "1.1.2"
assert expandvars.__version__ == "v1.1.2"
module = pathlib.Path(expandvars.__file__).resolve()
assert str(module).startswith("/usr/")
assert subprocess.check_output(["rpm", "-qf", "--qf", "%{NAME}", str(module)], text=True) == "python3-expandvars"
root = pathlib.Path("/usr/share/python-expandvars/tests")
assert len(list((root / "tests").glob("test_*.py"))) == 4
assert (root / "tests/data/foo.txt").read_bytes() == b"$FOO:${FOO}\n"
assert hashlib.sha256((root / "reference/expandvars.py").read_bytes()).digest() == hashlib.sha256(module.read_bytes()).digest()
for source in root.rglob("*"):
    assert not source.is_symlink()
    if source.is_file():
        assert subprocess.check_output(["rpm", "-qf", "--qf", "%{NAME}", str(source)], text=True) == "python3-expandvars"
PYTEST
cp -a /usr/share/python-expandvars/tests/tests /usr/share/python-expandvars/tests/reference /usr/share/python-expandvars/tests/pyproject.toml /usr/share/python-expandvars/tests/tox.ini /usr/share/python-expandvars/tests/uv.lock .
test ! -e expandvars.py
test ! -e expandvars
# The reference copy is lint input only, never a library import candidate.
black --diff .
PYTHONPATH=. python3 -m pytest --cov --cov-report=html --cov-fail-under=100
# Keep isolated coverage/test outputs for CI diagnostics.
