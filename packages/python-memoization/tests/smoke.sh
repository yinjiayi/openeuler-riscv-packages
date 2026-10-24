#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
rpm -q -- python-memoization
# Test-only prerequisite: the fresh base image does not retain BuildRequires.
[[ $(pwd -P) == /workspace ]]
[[ -f artifacts/repository/resolution.json ]]
if [[ -d artifacts/smoke ]]; then test_evidence_dir=artifacts/smoke; elif [[ -d artifacts/golden/python-memoization ]]; then test_evidence_dir=artifacts/golden/python-memoization; else exit 2; fi
[[ ! -e $test_evidence_dir/memoization-test-prerequisites.json ]]
printf 'd62f6ec90fa3a5c5112ad4cd364d7a75ef69778c2a432825add4164a1bd64eca  ci/run-dnf-transaction\n' | sha256sum --check --strict
python3 ci/run-dnf-transaction --evidence "$test_evidence_dir/memoization-test-prerequisites.json" --budget-seconds 300 --attempt-timeouts-seconds 290 --retry-delay-seconds 0 --kill-after-seconds 10 -- dnf -y --setopt=install_weak_deps=False --disablerepo='*' --enablerepo=openeuler-rva23 install -- python3-coverage-7.3.2-1.oe2403sp3.riscv64
[[ $(rpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}' -- python3-coverage) == python3-coverage-7.3.2-1.oe2403sp3.riscv64 ]]
env -u PYTHONHOME -u PYTHONSTARTUP -u PYTHONPATH -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u COVERAGE_PROCESS_START python3 - /usr/share/python-memoization/original /usr/lib/python3.11/site-packages installed <<'PY'
# SPDX-License-Identifier: Apache-2.0
"""Target-only original coverage run test.py route; never executed locally."""
import ast, hashlib, importlib, importlib.abc, importlib.machinery, importlib.metadata
import json, os, pathlib, runpy, shutil, subprocess, sys, tempfile, unittest

original = pathlib.Path(sys.argv[1]).resolve()
site = pathlib.Path(sys.argv[2]).resolve()
mode = sys.argv[3]
assert mode in ('wheel', 'buildroot', 'installed') and sys.version_info[:2] == (3, 11)
manifest = json.loads((original.parent / 'original-files.json').read_bytes())
assert len(manifest) == 53
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for name, digest in manifest.items():
    p = original / name
    assert p.is_file() and not p.is_symlink() and sha(p) == digest
archive = original.parent / 'python-memoization-0.4.0.tar.gz'
license_file = original.parent / 'PYTHON-3.7.2-LICENSE.txt'
assert sha(archive) == 'd203d15acef5b1714c5835c7e3c0094cbbe7640b0220a3e5a014ef9180706937'
assert sha(license_file) == 'b9a6d9320b8f2693e8d41e496ce56caadacaddcca9be2a64a61749278f425cf2'
for key in ('PYTHONHOME', 'PYTHONSTARTUP', 'PYTHONPATH', 'PYTEST_ADDOPTS', 'PYTEST_PLUGINS', 'COVERAGE_PROCESS_START'):
    os.environ.pop(key, None)
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
if mode == 'installed':
    for p in [archive, license_file, original.parent / 'original-files.json', *[original / n for n in manifest]]:
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '--', str(p)], text=True).strip() == 'python-memoization'
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '--', str(pathlib.Path(sys.executable).resolve())], text=True).strip() == 'python3'
os.environ['PYTHONPATH'] = str(site)
sys.path[:] = [str(site)] + [p for p in sys.path if p and not pathlib.Path(p).resolve().is_relative_to(original)]
assert importlib.metadata.version('memoization') == '0.4.0'
coverage_module = importlib.import_module('coverage')
coverage_origin = pathlib.Path(coverage_module.__file__).resolve()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '--', str(coverage_origin)], text=True).strip() == 'python3-coverage'
coverage_version = importlib.metadata.version('coverage')
assert coverage_version == '7.3.2'
coverage_rpm = subprocess.check_output(['rpm', '-q', '--qf', '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}', '--', 'python3-coverage'], text=True).strip()
assert coverage_rpm == 'python3-coverage-7.3.2-1.oe2403sp3.riscv64'
package = site / 'memoization'
payload = {n.removeprefix('memoization/'): h for n, h in manifest.items() if n.startswith('memoization/')}
assert len(payload) == 42
actual = {str(p.relative_to(package)) for p in package.rglob('*') if p.is_file() and p.suffix != '.pyc'}
assert actual == set(payload)
for name, digest in payload.items():
    p = package / name
    assert not p.is_symlink() and sha(p) == digest
    if mode == 'installed':
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%{NAME}', '--', str(p)], text=True).strip() == 'python-memoization'
modules = {}
for name in payload:
    if not name.endswith('.py'): continue
    parts = pathlib.PurePosixPath(name).with_suffix('').parts
    fullname = '.'.join(('memoization',) + (parts[:-1] if parts[-1] == '__init__' else parts))
    modules[fullname] = name
tree = ast.parse((original / 'test.py').read_bytes())
methods = {c.name + '.' + n.name for c in tree.body if isinstance(c, ast.ClassDef) for n in c.body if isinstance(n, ast.FunctionDef) and n.name.startswith('test')}
assert len(methods) == 25
guarded = {}
def stop(reason):
    print('MEMOIZATION_ORIGIN_VIOLATION ' + str(reason), file=sys.stderr, flush=True)
    os._exit(86)
class Loader(importlib.abc.Loader):
    def __init__(self, underlying, fullname): self.underlying, self.fullname = underlying, fullname
    def create_module(self, spec): return self.underlying.create_module(spec) if hasattr(self.underlying, 'create_module') else None
    def exec_module(self, module):
        self.underlying.exec_module(module)
        p = pathlib.Path(module.__file__).resolve()
        if p != (package / modules[self.fullname]).resolve() or sha(p) != payload[modules[self.fullname]]: stop(self.fullname)
        guarded[self.fullname] = str(p)
class Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'memoization' or fullname.startswith('memoization.'):
            if fullname not in modules: stop('unexpected namespace ' + fullname)
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)
            p = (package / modules[fullname]).resolve()
            if spec is None or not spec.origin or pathlib.Path(spec.origin).resolve() != p or sha(p) != payload[modules[fullname]]: stop('bad spec ' + fullname)
            spec.loader = Loader(spec.loader, fullname)
            return spec
def audit(event, args):
    if event == 'exec':
        filename = getattr(args[0], 'co_filename', '')
        if filename and not filename.startswith('<'):
            p = pathlib.Path(filename).resolve()
            if p.is_relative_to(original / 'memoization'): stop('original runtime exec ' + filename)
            if p.is_relative_to(package):
                rel = str(p.relative_to(package))
                if rel not in payload or sha(p) != payload[rel]: stop('bad runtime exec ' + filename)
sys.meta_path.insert(0, Finder())
sys.addaudithook(audit)
importlib.import_module('memoization.memoization')
assert guarded.get('memoization') and guarded.get('memoization.memoization')
# Verify first, then unload the verified namespace so original coverage captures
# runtime discovery while the same fail-closed guard remains installed.
for name in tuple(sys.modules):
    if name == 'memoization' or name.startswith('memoization.'): del sys.modules[name]
seen, results = [], []
real_start = unittest.TestResult.startTest
def start_test(self, test):
    seen.append(test.id())
    return real_start(self, test)
unittest.TestResult.startTest = start_test
real_run = unittest.TextTestRunner.run
def run_suite(self, suite):
    result = real_run(self, suite)
    results.append(result)
    return result
unittest.TextTestRunner.run = run_suite
with tempfile.TemporaryDirectory(prefix='memoization-default-') as scratch:
    work = pathlib.Path(scratch)
    for name in ('test.py', '.coveragerc'):
        shutil.copy2(original / name, work / name)
        assert sha(work / name) == manifest[name]
    os.chdir(work)
    sys.argv = ['coverage', 'run', 'test.py']
    try:
        runpy.run_module('coverage', run_name='__main__', alter_sys=False)
    except SystemExit as exc:
        assert exc.code in (None, 0)
    assert len(results) == 1 and results[0].testsRun == 25 and results[0].wasSuccessful()
    assert not results[0].skipped and not results[0].expectedFailures and not results[0].unexpectedSuccesses
    assert len(seen) == 25 and {n.removeprefix('__main__.') for n in seen} == methods
    assert sha(work / 'test.py') == manifest['test.py'] and sha(work / '.coveragerc') == manifest['.coveragerc']
    data = work / '.coverage'
    assert data.is_file() and data.stat().st_size > 0
    print('MEMOIZATION_DEFAULT_REPORT ' + json.dumps(dict(mode=mode, command='coverage run test.py', testsRun=results[0].testsRun, test_ids=seen, skips=0, failures=0, errors=0, coverage_tool=dict(origin=str(coverage_origin),version=coverage_version,rpm=coverage_rpm, invocation='coverage.__main__ via runpy; original argv preserved, not a bare launcher claim'),coverage_data_sha256=sha(data), coverage_numeric_claim=False, origins=guarded, external_coveralls_upload='excluded/unclaimed'), sort_keys=True))
PY
