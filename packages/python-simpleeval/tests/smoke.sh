#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-simpleeval
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONHOME PYTHONPATH
python3 - <<'PY'
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

root = Path('/usr/share/python-simpleeval')
archive = root / 'upstream.tar.gz'
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert digest(archive) == '8f1849cb8668b828b480c8be2723eff90003a9872136479b2a77a6ce3f984c0e'
def owned(path):
    assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '--', str(path)], text=True).strip() == 'python-simpleeval'
owned(archive)
with tarfile.open(archive, 'r:gz') as tar:
    rows = []
    top = None
    for member in tar.getmembers():
        p = Path(member.name)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in member.name and '\x00' not in member.name
        assert member.isdir() or member.isfile()
        if top is None:
            top = p.parts[0]
        assert p.parts[0] == top
        if member.isfile():
            relative = Path(*p.parts[1:])
            retained = root / 'original' / relative
            assert retained.is_file() and not retained.is_symlink()
            assert hashlib.sha256(tar.extractfile(member).read()).hexdigest() == digest(retained)
            owned(retained)
            rows.append(str(relative))
assert len(rows) == 36 and len(set(rows)) == 36
retained_files = {str(p.relative_to(root/'original')) for p in (root/'original').rglob('*') if p.is_file()}
generated = retained_files - set(rows)
assert all('/__pycache__/' in '/' + p and p.endswith('.pyc') for p in generated)
assert set(rows).issubset(retained_files)
spec = importlib.util.find_spec('simpleeval')
assert spec and spec.origin
runtime = Path(spec.origin).resolve()
assert runtime.name == 'simpleeval.py' and '/site-packages/' in str(runtime)
assert root not in runtime.parents
assert digest(runtime) == 'e5f725e0dad1cd27b846263b024efd88cde59b14d5a1670dd491a2bc9d05dcd7'
owned(runtime)
import importlib.metadata
assert importlib.metadata.version('simpleeval') == '1.0.8'
scratch = Path(tempfile.mkdtemp(prefix='simpleeval-installed-'))
shutil.copytree(root/'original/tests', scratch/'tests')
assert len(list((scratch/'tests').glob('*.py'))) == 24
for path in (scratch/'tests').glob('*.py'):
    assert digest(path) == digest(root/'original/tests'/path.name)
assert not (scratch/'simpleeval.py').exists()
guard = scratch/'import-guard'
guard.mkdir()
# Verify normal runtime selection without replacing its loader or source.
code = '''import hashlib, importlib.machinery, pathlib, sys
class InstalledOriginGuard:
    @staticmethod
    def find_spec(fullname, path=None, target=None):
        if fullname == "simpleeval":
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)
            assert spec is not None and pathlib.Path(spec.origin).resolve() == pathlib.Path(%r)
            assert hashlib.sha256(pathlib.Path(spec.origin).read_bytes()).hexdigest() == %r
        return None
sys.meta_path.insert(0, InstalledOriginGuard)
''' % (str(runtime), digest(runtime))
(guard/'sitecustomize.py').write_text(code)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONNOUSERSITE='1', PYTHONPATH=str(guard))
env.pop('PYTHONHOME', None)
for command in [
    ['python3', '-Werror', '-m', 'unittest'],
    ['python3', '-m', 'coverage', 'run', '-m', 'unittest'],
    ['python3', '-m', 'coverage', 'xml'],
]:
    subprocess.run(command, cwd=scratch, env=env, check=True)
print(json.dumps({'runtime': str(runtime), 'original_files': len(rows), 'original_tests': 'complete unmodified collection', 'entrypoint': 'coverage.cmdline:main via python3 -m coverage'}))
PY
