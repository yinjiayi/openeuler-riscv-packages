#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-dotmap python3-pytest
unset PYTHONPATH
test_root=/usr/share/python-dotmap
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
python3 - <<'PY'
import ast
import hashlib
import importlib.metadata
from pathlib import Path
import subprocess
import dotmap

assert importlib.metadata.version('dotmap') == '1.3.30'
module = Path(dotmap.__file__).resolve()
assert str(module).startswith('/usr/lib/') and module.parent.name == 'dotmap' and module.name == '__init__.py'
owned = Path('/usr/share/python-dotmap')
for path in sorted(owned.rglob('*')):
    assert not path.is_symlink()
    if path.is_file():
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(path)], text=True) == 'python-dotmap'
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(module)], text=True) == 'python-dotmap'
assert hashlib.sha256(module.read_bytes()).hexdigest() == 'cdc16a3a25d4da7f740bfbc277e0ad70ac41079f9788ec8c9a57ecd0b776b51e'
assert module.read_bytes() == (owned / 'reference' / '__init__.py').read_bytes()
suite = owned / 'tests' / 'test.py'
assert {p.name for p in suite.parent.iterdir()} == {'test.py'}
assert hashlib.sha256(suite.read_bytes()).hexdigest() == '61829d3ec1e81a816f855ca2af57a9a9b70575ee7d3364409e638ad5e62e48f1'
assert sum(isinstance(n, ast.FunctionDef) and n.name.startswith('test') for n in ast.walk(ast.parse(suite.read_bytes()))) == 29
assert suite.read_bytes() == (module.parent / 'test.py').read_bytes()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(module.parent / 'test.py')], text=True) == 'python-dotmap'
for name in ('setup.py', 'setup.cfg', 'MANIFEST.in', 'Makefile', 'requirements.txt', '.travis.yml'):
    assert (owned / name).is_file()
print('RPM-owned installed Dotmap 1.3.30 and complete byte-identical 29-method suite verified')
PY
# The original unittest discovery command sees the whole original test.py
# at a writable tests-only root; there is no copied dotmap runtime package.
mkdir unittest
cp "$test_root/tests/test.py" unittest/test.py
cd unittest
test ! -e dotmap
python3 -m unittest
cd "$scratch"
# Preserve the original pytest file argument. This directory has no
# __init__.py or library code and cannot shadow the installed regular package.
mkdir -p pytest/dotmap
cp "$test_root/tests/test.py" pytest/dotmap/test.py
test ! -e pytest/dotmap/__init__.py
cd pytest
pytest dotmap/test.py
