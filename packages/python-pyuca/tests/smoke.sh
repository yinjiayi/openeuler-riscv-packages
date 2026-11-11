#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
export PIP_NO_INDEX=1 PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1
rpm -q -- python-pyuca python3-flake8 python3-coverage
python3 - <<'PY'
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

shared = Path('/usr/share/python-pyuca')
archive = shared / 'upstream.tar.gz'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(archive) == 'e1e0880ffa05260a111e9d0652443f728896eee4a48448c1dff2cab276cf9435'
def owned(p):
    q = subprocess.run(['rpm', '-qf', '--qf', '%{NAME}\n', str(p)], check=True, capture_output=True, text=True)
    assert q.stdout.splitlines() == ['python-pyuca'], (str(p), q.stdout)
owned(archive)
with tempfile.TemporaryDirectory(prefix='pyuca-installed-') as temp:
    root = Path(temp)
    lint = root / 'original-lint'
    lint.mkdir()
    blobs = {}
    total = 0
    with tarfile.open(archive) as stream:
        members = stream.getmembers()
        assert {m.name.split('/')[0] for m in members} == {'pyuca-d751d694a90ab9d8789263822e02ae822d251e2c'}
        for m in members:
            assert not m.name.startswith('/') and '\\' not in m.name and '\0' not in m.name and '..' not in Path(m.name).parts
            assert not m.issym() and not m.islnk() and (m.isdir() or m.isfile())
            if m.isdir():
                continue
            rel = Path(*Path(m.name).parts[1:])
            assert rel.parts and str(rel) not in blobs
            raw = stream.extractfile(m).read()
            total += len(raw)
            assert len(raw) == m.size and total <= 181425190
            dst = lint / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(raw)
            blobs[str(rel)] = hashlib.sha256(raw).hexdigest()
    assert len(blobs) == 40 and total == 181425190
    for rel, expected in blobs.items():
        retained = shared / 'original' / rel
        assert digest(retained) == expected
        owned(retained)
    # Whole original lint includes unchanged runtime, tests and every fixture.
    subprocess.run(['flake8', '.'], cwd=lint, check=True)
    package = importlib.import_module('pyuca')
    installed = Path(package.__file__).resolve().parent
    assert installed.name == 'pyuca' and installed.parent.name == 'site-packages'
    runtime = {rel.removeprefix('pyuca/'): expected for rel, expected in blobs.items() if rel.startswith('pyuca/')}
    assert len(runtime) == 9 and sum(rel.startswith('allkeys-') for rel in runtime) == 5
    for rel, expected in runtime.items():
        path = installed / rel
        assert digest(path) == expected
        owned(path)
    scratch = root / 'installed-default'
    scratch.mkdir()
    for rel, expected in blobs.items():
        if rel.startswith('pyuca/'):
            continue
        dst = scratch / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((lint / rel).read_bytes())
    assert not (scratch / 'pyuca').exists()
    # Doctest keeps its exact original argument but reads the RPM-owned file.
    (scratch / 'pyuca').mkdir()
    (scratch / 'pyuca/utils.py').symlink_to(installed / 'utils.py')
    assert not (scratch / 'pyuca/__init__.py').exists()
    assert (scratch / 'pyuca/utils.py').resolve() == installed / 'utils.py'
    guard = root / 'guard'
    guard.mkdir()
    guard_code = '''import builtins, hashlib, sys
from pathlib import Path
EXPECTED = %r
INSTALLED = Path(%r)
old = builtins.__import__
def checked(name, globals=None, locals=None, fromlist=(), level=0):
    value = old(name, globals, locals, fromlist, level)
    for key, module in list(sys.modules.items()):
        if key == 'pyuca' or key.startswith('pyuca.'):
            path = Path(module.__file__).resolve()
            assert path.parent == INSTALLED and path.name in EXPECTED
            assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED[path.name]
    return value
builtins.__import__ = checked
''' % ({rel: expected for rel, expected in runtime.items() if rel.endswith('.py')}, str(installed))
    (guard / 'sitecustomize.py').write_text(guard_code)
    env = dict(os.environ, PYTHONPATH=str(guard), PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1')
    commands = [
        ['python3', '-m', 'coverage', 'run', '--branch', '--source', str(installed), 'test.py'],
        ['python3', '-m', 'coverage', 'run', '--append', '--branch', '--source', str(installed), '-m', 'doctest', 'pyuca/utils.py'],
        ['python3', '-m', 'coverage', 'run', '--append', '--branch', '--source', str(installed), 'full_test.py'],
    ]
    # The scratch pyuca directory is only the original doctest argument's alias.
    # Select the verified installed tree, not that existing scratch directory.
    assert not (scratch / '.coverage').exists()
    for command in commands:
        subprocess.run(command, cwd=scratch, env=env, check=True)
    subprocess.run(['python3', '-m', 'coverage', 'report'], cwd=scratch, env=env, check=True)
    report = scratch / 'installed-coverage.json'
    assert not report.exists()
    subprocess.run(['python3', '-m', 'coverage', 'json', '-o', str(report)], cwd=scratch, env=env, check=True)
    measured = json.loads(report.read_text())
    assert measured['meta']['version'] == '7.3.2' and measured['meta']['branch_coverage'] is True
    expected_modules = {installed / rel: expected for rel, expected in runtime.items() if rel.endswith('.py')}
    assert len(expected_modules) == 4
    measured_modules = {}
    for filename, details in measured['files'].items():
        path = Path(filename)
        path = (path if path.is_absolute() else scratch / path).resolve()
        assert path in expected_modules and path not in measured_modules
        assert digest(path) == expected_modules[path]
        owned(path)
        assert details['executed_lines'] and details['summary']['covered_lines'] > 0
        measured_modules[path] = {'sha256': expected_modules[path], 'rpm_owner': 'python-pyuca', 'executed_lines': details['executed_lines'], 'summary': details['summary']}
    assert set(measured_modules) == set(expected_modules)
    assert measured['totals']['num_statements'] == 188 and measured['totals']['covered_lines'] > 0
    assert measured['totals']['num_branches'] > 0 and measured['totals']['covered_branches'] > 0
    print(json.dumps({'installed_measurement': 'fresh branch data for exact four SHA/RPM-owned modules', 'modules': {str(path): proof for path, proof in measured_modules.items()}, 'totals': measured['totals'], 'new_percentage_threshold': False}))
    for rel, expected in blobs.items():
        assert digest(lint / rel) == expected
    for rel, expected in runtime.items():
        assert digest(installed / rel) == expected
    print(json.dumps({'original_default': 'whole flake8 and coverage unit/doctest/full conformance passed', 'full_original_files': 40, 'full_original_bytes': total, 'installed_runtime_and_five_data_tables_rpm_owned': True, 'source_runtime_shadow': False, 'original_version_skips_retained': True, 'historical_matrix_or_performance_claimed': False}))
PY
