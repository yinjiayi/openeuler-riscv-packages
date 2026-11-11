#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
rpm -q -- python-decouple python3-pytest python3-mock
python3 - <<'PY'
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

shared = Path('/usr/share/python-decouple')
archive = shared / 'upstream.tar.gz'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(archive) == '977b3479b3fe087e49ecfd9196cc49f1613a67b66a3e1cea069bcf916dcf2ec2'
def owned(p):
    q = subprocess.run(['rpm', '-qf', '--qf', '%{NAME}\n', str(p)], check=True, capture_output=True, text=True)
    assert q.stdout.splitlines() == ['python-decouple'], (str(p), q.stdout)
owned(archive)
with tempfile.TemporaryDirectory(prefix='decouple-installed-') as temp:
    root = Path(temp)
    original = root / 'original'
    original.mkdir()
    blobs = {}
    with tarfile.open(archive) as stream:
        members = stream.getmembers()
        assert len({m.name.split('/')[0] for m in members}) == 1
        total = 0
        for m in members:
            assert not m.name.startswith('/') and '\\' not in m.name and '\0' not in m.name and '..' not in Path(m.name).parts
            assert not m.issym() and not m.islnk() and (m.isdir() or m.isfile())
            if m.isdir():
                continue
            rel = Path(*Path(m.name).parts[1:])
            assert rel.parts and str(rel) not in blobs
            raw = stream.extractfile(m).read()
            total += len(raw)
            assert len(raw) == m.size and total < 52428800
            dst = original / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
            blobs[str(rel)] = hashlib.sha256(raw).hexdigest()
    assert len(blobs) == 30
    assert sum(x.name.startswith('test_') for p in original.glob('tests/test_*.py') for x in ast.walk(ast.parse(p.read_bytes())) if isinstance(x, ast.FunctionDef)) == 57
    package = importlib.import_module('decouple')
    installed = Path(package.__file__).resolve()
    assert installed.name == 'decouple.py' and installed.parent.name == 'site-packages'
    assert digest(installed) == blobs['decouple.py']
    owned(installed)
    scratch = root / 'installed-default'
    scratch.mkdir()
    for rel, expected in blobs.items():
        retained = shared / 'original' / rel
        assert digest(retained) == expected
        owned(retained)
        if rel == 'decouple.py':
            continue
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(retained.read_bytes())
    assert not (scratch / 'decouple.py').exists()
    guard = root / 'guard'
    guard.mkdir()
    guard_code = '''import builtins, hashlib, sys
from pathlib import Path
EXPECTED = %r
INSTALLED = Path(%r)
old = builtins.__import__
def checked(name, globals=None, locals=None, fromlist=(), level=0):
    value = old(name, globals, locals, fromlist, level)
    if 'decouple' in sys.modules:
        path = Path(sys.modules['decouple'].__file__).resolve()
        assert path == INSTALLED and hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED
    return value
builtins.__import__ = checked
''' % (blobs['decouple.py'], str(installed))
    (guard / 'sitecustomize.py').write_text(guard_code)
    env = dict(os.environ, PYTHONPATH=str(guard), PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1')
    subprocess.run(['py.test'], cwd=scratch, env=env, check=True)
    assert all(digest(original / rel) == expected for rel, expected in blobs.items())
    assert digest(installed) == blobs['decouple.py']
    print(json.dumps({'installed_default': 'whole original py.test passed', 'static_test_functions': 57, 'full_original_files': 30, 'installed_runtime_rpm_owned': True, 'source_runtime_shadow': False, 'historical_tool_pins_or_matrix_claimed': False}))
PY
