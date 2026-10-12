#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
rpm -q -- python-configargparse python3-devel python3-black python3-mock python3-toml python3-pyyaml python3-pytest python3-pytest-cov python3-pytest-subtests python3-coverage
python3 - <<'PY'
import configargparse
import hashlib
import importlib.metadata
import inspect
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import test.test_argparse

assert inspect.getsource(test.test_argparse)
assert importlib.metadata.version('ConfigArgParse') == '1.8.0'
archive = Path('/usr/share/python-configargparse/upstream.tar.gz')
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(archive) == '910e8bd128e94a1ba3befad1549a5cece5285b7bc89fae6c0b713783088aaa55'
def owned(p):
    q = subprocess.run(['rpm', '-qf', '--qf', '%{NAME}\\n', str(p)], check=True, capture_output=True, text=True)
    assert q.stdout.splitlines() == ['python-configargparse'], (str(p), q.stdout)
owned(archive)
runtime = Path(configargparse.__file__).resolve()
owned(runtime)
with tempfile.TemporaryDirectory(prefix='configargparse-original-') as temp:
    top = Path(temp)
    original = top / 'original'
    original.mkdir()
    blobs = {}
    with tarfile.open(archive, 'r:gz') as stream:
        members = stream.getmembers()
        assert len({m.name.split('/')[0] for m in members}) == 1
        for m in members:
            assert not m.name.startswith('/') and '..' not in Path(m.name).parts
            assert not m.issym() and not m.islnk() and (m.isdir() or m.isfile())
            if m.isdir():
                continue
            rel = Path(*Path(m.name).parts[1:])
            assert rel.parts and str(rel) not in blobs
            raw = stream.extractfile(m).read()
            assert len(raw) == m.size
            path = original / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
            blobs[str(rel)] = hashlib.sha256(raw).hexdigest()
    assert len(blobs) == 17
    assert digest(runtime) == blobs['configargparse.py']
    # Only temporary source runtime moves outside collection; every test stays.
    isolated = top / 'source-runtime.py'
    (original / 'configargparse.py').rename(isolated)
    assert digest(isolated) == blobs['configargparse.py']
    guard = top / 'guard'
    guard.mkdir()
    code = '''import builtins, hashlib, sys
from pathlib import Path
EXPECTED = %r
RUNTIME = Path(%r)
old = builtins.__import__
def checked(name, globals=None, locals=None, fromlist=(), level=0):
    value = old(name, globals, locals, fromlist, level)
    mod = sys.modules.get('configargparse')
    if mod is not None:
        path = Path(mod.__file__).resolve()
        assert path == RUNTIME
        assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED
    return value
builtins.__import__ = checked
''' % (blobs['configargparse.py'], str(runtime))
    (guard / 'sitecustomize.py').write_text(code)
    env = dict(os.environ, PYTHONPATH=str(guard), PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1')
    subprocess.run(['pytest', '--cov-branch', '--cov-context=test', '--cov=.'], cwd=original, env=env, check=True)
    assert all(digest(original / rel) == value for rel, value in blobs.items() if rel != 'configargparse.py')
    assert digest(isolated) == digest(runtime) == blobs['configargparse.py']
    owned(runtime)
    print(json.dumps({'installed_default': 'whole original Python3.11 pytest coverage argv passed', 'source_runtime_shadow': False, 'original_blobs': 17, 'stdlib_argparse_compatibility_required': True, 'other_interpreter_lint_or_platform_matrix_claimed': False, 'installed_coverage_percentage_claimed': False}))
PY
