#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
rpm -q -- python-ratelimit python3-pytest python3-pytest-cov python3-pylint
python3 - <<'PY'
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

shared = Path('/usr/share/python-ratelimit')
archive = shared / 'upstream.tar.gz'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(archive) == '9ecb5a42d0206f234e2a568f246a2cb52b3aa1f54432d3e85839bb637db97f53'
def owned(p):
    q = subprocess.run(['rpm', '-qf', '--qf', '%{NAME}\n', str(p)], check=True, capture_output=True, text=True)
    assert q.stdout.splitlines() == ['python-ratelimit'], (str(p), q.stdout)
owned(archive)
with tempfile.TemporaryDirectory(prefix='ratelimit-original-') as temp:
    root = Path(temp)
    original = root / 'original'
    original.mkdir()
    blobs = {}
    with tarfile.open(archive) as stream:
        members = stream.getmembers()
        assert len({m.name.split('/')[0] for m in members}) == 1
        for m in members:
            assert not m.name.startswith('/') and '..' not in Path(m.name).parts
            assert not m.issym() and not m.islnk() and (m.isdir() or m.isfile())
            if m.isdir():
                continue
            rel = Path(*Path(m.name).parts[1:])
            assert str(rel) not in blobs and rel.parts
            raw = stream.extractfile(m).read()
            assert len(raw) == m.size
            dest = original / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            blobs[str(rel)] = hashlib.sha256(raw).hexdigest()
    assert len(blobs) == 15
    runtime = {k: v for k, v in blobs.items() if k.startswith('ratelimit/') and k.endswith('.py')}
    tests = {k: v for k, v in blobs.items() if k.startswith('tests/') and k.endswith('.py')}
    assert len(runtime) == 3 and len(tests) == 3
    assert sum(x.name.startswith('test_') for p in original.glob('tests/unit/*.py') for x in ast.walk(ast.parse(p.read_bytes())) if isinstance(x, ast.FunctionDef)) == 4
    package = importlib.import_module('ratelimit')
    site = Path(package.__file__).resolve().parent.parent
    for rel, expected in runtime.items():
        installed = site / rel
        assert digest(installed) == expected
        owned(installed)
    scratch = root / 'installed-default'
    scratch.mkdir()
    retained = dict(tests)
    retained.update({k: blobs[k] for k in ('pytest.ini', 'requirements.txt', 'setup.py', '.pylintrc', '.travis.yml', 'MANIFEST.in', 'README.rst', 'LICENSE.txt')})
    for rel, expected in retained.items():
        installed = shared / rel
        assert digest(installed) == expected
        owned(installed)
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(installed.read_bytes())
    # Alias the physical installed directory for unchanged doctest collection;
    # never copy the source runtime or select a subset of original tests.
    (scratch / 'ratelimit').symlink_to(site / 'ratelimit', target_is_directory=True)
    assert (scratch / 'ratelimit').resolve() == (site / 'ratelimit').resolve()
    guard = root / 'guard'
    guard.mkdir()
    guard_code = '''import builtins, hashlib, sys
from pathlib import Path
EXPECTED = %r
SITE = Path(%r)
old = builtins.__import__
def checked(name, globals=None, locals=None, fromlist=(), level=0):
    value = old(name, globals, locals, fromlist, level)
    for key, mod in list(sys.modules.items()):
        if key == 'ratelimit' or key.startswith('ratelimit.'):
            path = Path(mod.__file__).resolve()
            relative = str(path.relative_to(SITE))
            assert relative in EXPECTED
            assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED[relative]
    return value
builtins.__import__ = checked
''' % (runtime, str(site))
    (guard / 'sitecustomize.py').write_text(guard_code)
    env = dict(os.environ, PYTHONPATH=str(guard), PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1')
    subprocess.run(['py.test'], cwd=scratch, env=env, check=True)
    assert all(digest(original / rel) == expected for rel, expected in blobs.items())
    assert all(digest(site / rel) == expected for rel, expected in runtime.items())
    print(json.dumps({'installed_default': 'whole original py.test doctest/coverage passed', 'static_test_methods': 4, 'runtime_files': 3, 'historical_exact_pins_or_matrix_claimed': False, 'source_runtime_shadow': False}))
PY
