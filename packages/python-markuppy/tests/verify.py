#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0
"""Run the unchanged original default suite against staged or RPM-owned code."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def digest(path):
    assert path.is_file() and not path.is_symlink(), str(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert len(sys.argv) == 4 and sys.argv[3] in ('buildroot', 'installed')
    assert (3, 11) <= sys.version_info[:2] < (3, 12), sys.version
    root, site = (Path(p).resolve() for p in sys.argv[1:3])
    installed = sys.argv[3] == 'installed'
    manifest = json.loads((root / 'original-files.json').read_text())
    assert len(manifest) == 13
    original = root / 'original'

    def owned(path):
        if installed:
            assert subprocess.check_output(
                ['rpm', '-qf', '--qf', '%{NAME}', str(path)], text=True
            ) == 'python-markuppy'

    for rel, row in manifest.items():
        p = original / rel
        assert digest(p) == row['sha256'], rel
        # RPM's brp scripts may add bytecode, not change retained source bytes.
        assert row['mode'] in (0o644, 0o755) and p.stat().st_mode & 0o777 == 0o644, rel
        owned(p)
    archive = root / 'markuppy-1.18.tar.gz'
    assert digest(archive) == '9c7ba86d5d9fb7b2b4be71c55496a18742c300eeff08e3e07895e92db07fc98d'
    owned(archive)
    owned(root / 'original-files.json')
    owned(root / 'verify.py')
    runtime = {p.removeprefix('MarkupPy/'): r['sha256']
               for p, r in manifest.items() if p.startswith('MarkupPy/')}
    assert set(runtime) == {'__init__.py', 'markup.py'}
    for rel, expected in runtime.items():
        p = site / 'MarkupPy' / rel
        assert digest(p) == expected, str(p)
        owned(p)
    distributions = [d for d in importlib.metadata.distributions(path=[str(site)])
                     if re.sub(r'[-_.]+', '-', d.metadata['Name']).lower() == 'markuppy']
    assert len(distributions) == 1 and distributions[0].version == '1.18'
    for name in ('METADATA', 'WHEEL', 'RECORD'):
        owned(distributions[0]._path / name)
    # Fail closed for a new unexpected runtime source; normal RPM bytecode is allowed.
    for p in (site / 'MarkupPy').rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(site / 'MarkupPy').as_posix()
        assert rel in runtime or (p.parent.name == '__pycache__' and
               p.suffix == '.pyc' and any(p.name.startswith(Path(x).stem + '.')
                                         for x in runtime)), rel
        owned(p)

    guard = '''import hashlib,importlib.abc,importlib.machinery,pathlib,sys,runpy
site=pathlib.Path(SITE);runtime=RUNTIME
class OriginGuard(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname=='MarkupPy' or fullname.startswith('MarkupPy.'):
            spec=importlib.machinery.PathFinder.find_spec(fullname,path)
            assert spec and spec.origin,(fullname,spec)
            p=pathlib.Path(spec.origin).resolve()
            rel=p.relative_to(site/'MarkupPy').as_posix()
            assert rel in runtime and hashlib.sha256(p.read_bytes()).hexdigest()==runtime[rel]
            return spec
        return None
sys.meta_path.insert(0,OriginGuard())
sys.path.insert(0,str(site))
sys.path.insert(0,TESTS)
sys.argv=[RUNNER]
runpy.run_path(RUNNER,run_name='__main__')
'''.replace('SITE', repr(str(site))).replace('RUNTIME', repr(runtime))
    with tempfile.TemporaryDirectory(prefix='markuppy-original-defaults-') as scratch:
        work = Path(scratch)
        tests = work / 'tests'
        tests.mkdir()
        for rel, row in manifest.items():
            if rel.startswith('tests/'):
                shutil.copyfile(original / rel, work / rel)
                assert digest(work / rel) == row['sha256']
        assert len(list(tests.iterdir())) == 3 and not (work / 'MarkupPy').exists()
        runner = tests / 'run_tests.py'
        code = guard.replace('TESTS', repr(str(tests))).replace('RUNNER', repr(str(runner)))
        env = {k: v for k, v in os.environ.items()
               if not k.startswith('PYTHON') and k not in ('HOME',)}
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        result = subprocess.run([sys.executable, '-I', '-B', '-c', code], cwd=work,
                                env=env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, check=False)
        print(result.stdout, end='')
        assert result.returncode == 0, result.returncode
        completed = re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. ok$', result.stdout, re.M)
        assert len(completed) == len(set(completed)) == 9, completed
        assert re.search(r'^Ran 9 tests in ', result.stdout, re.M)
        assert re.search(r'^OK\s*$', result.stdout, re.M)
        assert not re.search(r'\b(?:skipped|FAILED|ERROR|FAIL)\b', result.stdout)
    for rel, expected in runtime.items():
        assert digest(site / 'MarkupPy' / rel) == expected
    print(json.dumps(dict(original_default_runner='tests/run_tests.py', tests=9,
                          skips=0, runtime_origin=str(site / 'MarkupPy'),
                          engine='installed-RPM' if installed else 'buildroot-wheel',
                          python=sys.version.split()[0])))


if __name__ == '__main__':
    main()
