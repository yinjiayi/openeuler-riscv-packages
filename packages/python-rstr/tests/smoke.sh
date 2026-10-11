#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-rstr python3-mypy
unset PYTHONPATH
test_root=/usr/share/python-rstr
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
cd "$scratch"
python3 - <<'PY'
import hashlib
import importlib.metadata
from pathlib import Path
import subprocess
import rstr

assert importlib.metadata.version('rstr') == '3.2.2'
module_root = Path(rstr.__file__).resolve().parent
assert str(module_root).startswith('/usr/lib/') and module_root.name == 'rstr'
owned_root = Path('/usr/share/python-rstr')
expected_tests = {'__init__.py', 'test_package_level_access.py', 'test_rstr.py', 'test_xeger.py'}
assert {p.name for p in (owned_root / 'tests').iterdir()} == expected_tests
for path in sorted(owned_root.rglob('*')):
    assert not path.is_symlink()
    if path.is_file():
        owner = subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(path)], text=True)
        assert owner == 'python-rstr', (path, owner)
expected_modules = {'__init__.py', 'rstr_base.py', 'xeger.py', 'py.typed'}
assert {p.name for p in (owned_root / 'reference' / 'rstr').iterdir()} == expected_modules
for source in sorted((owned_root / 'reference' / 'rstr').iterdir()):
    installed = module_root / source.name
    assert installed.is_file() and not installed.is_symlink()
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', str(installed)], text=True) == 'python-rstr'
    assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(installed.read_bytes()).digest()
for name in ('pyproject.toml', 'tox.ini'):
    assert (owned_root / name).is_file()
print('RPM-owned installed rstr 3.2.2 and complete byte-identical typing reference verified')
PY
# This unittest directory has tests/config only, never a source-library shadow.
cp -a "$test_root/tests" .
cp "$test_root/pyproject.toml" "$test_root/tox.ini" .
test ! -e rstr
PYTHONPATH=. python3 -m unittest
# The byte-identical RPM-owned reference is static mypy input in a separate
# directory. It is never imported by runtime unittest discovery.
mkdir typing
cp -a "$test_root/reference/rstr" typing/
cp "$test_root/pyproject.toml" "$test_root/tox.ini" typing/
cd typing
mypy --strict rstr
