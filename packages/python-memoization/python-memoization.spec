# SPDX-License-Identifier: Apache-2.0
Name:           python-memoization
Version:        0.4.0
Release:        1%{?dist}
Summary:        Function memoization with TTL and configurable cache algorithms
License:        MIT AND Python-2.0
URL:            https://github.com/lonelyenvoy/python-memoization
Source0:        python-memoization-0.4.0.tar.gz
Source1:        PYTHON-3.7.2-LICENSE.txt
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools
BuildRequires:  python3-coverage
Requires:       python3 >= 3.4
Requires:       python3 < 4

%description
Function memoization with TTL, custom keys and FIFO/LRU/LFU caching. Complete
upstream source, original tests/configuration and all derivative licenses kept.

%prep
%setup -q -n python-memoization-9c1a0d13e8fbad1f7f4a05d5b41873a7ca5b6aaa
mkdir -p ../memoization-pristine
cp -a . ../memoization-pristine/
cp -p %{SOURCE1} PYTHON-3.7.2-LICENSE.txt
cat > MEMOIZATION-ATTRIBUTION.txt <<'NOTICE'
Memoization0.4.0 retains its complete upstream MIT license and notices.
Python-derived material is redistributed with the complete fixed CPython3.7.2
historical LICENSE (PSF/BeOpen/CNRI/CWI) and corresponding copyright notices.
Official reference: https://github.com/python/cpython/tree/9a3ffc0492d1310ead9ce8f5ee678c26b20a338d
memoization/backport/backport_enum.py matches official Lib/enum.py apart from
three added header lines identifying its Python3.7.2 provenance. All53 upstream
files remain unchanged. It is shipped even when CPython3.11 uses stdlib enum.
README states the library is based on functools. HashedList adapts _HashedSeq
(renamed attribute, caller-provided hash); key creation and cache wrappers add
typed/unhashable keys, TTL, custom keys, argument maps and FIFO/LFU/API extensions
to related functools structures. The fixed reference proves observed lineage,
not a unique historical copy version/date or a license waiver.
Original LFU paper/Medium algorithm citations remain in lfu_cache.py unchanged.
No upstream or Python trademark/author endorsement is asserted.
Recipe/guard helpers have separate Apache-2.0 scope, not upstream relicensing.
NOTICE

%build
SOURCE_DATE_EPOCH=315532800 %{__python3} -m pip wheel --no-index --no-deps --no-build-isolation --wheel-dir wheelhouse .

%install
%{__python3} -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} wheelhouse/memoization-0.4.0-*.whl
install -d %{buildroot}%{_datadir}/python-memoization/original
cp -a ../memoization-pristine/. %{buildroot}%{_datadir}/python-memoization/original/
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/python-memoization/python-memoization-0.4.0.tar.gz
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/python-memoization/PYTHON-3.7.2-LICENSE.txt
install -m 0644 MEMOIZATION-ATTRIBUTION.txt %{buildroot}%{_datadir}/python-memoization/MEMOIZATION-ATTRIBUTION.txt
cat > %{buildroot}%{_datadir}/python-memoization/original-files.json <<'JSON'
{".coveragerc": "af38022f1ba923ac39aec79b06dfb952da19e61c0baf926fd17d711702abaf1b", ".gitignore": "e37c59ffb610e87912987b40c184ff3b8246a4abbde57ef064af8ebd31007187", ".mypy.ini": "5887a829594e6755d92ca07676824b7dd60c771c2c90c5675745e0fc50368ab3", ".travis.yml": "4ffafb0b8a35c27482d74c4fc88b11dc0e5f79d4e84a2a360e243a480b8d5fe2", "CONTRIBUTING.md": "7fdc9748fd6b979329a57b779ba9e67a73c77f7fa91e2b48a31b1f742ab7383f", "CONTRIBUTORS.md": "bf6161f88bf8739367f4707ad7908cf3208bbe26839e729667953d1500793a25", "LICENSE": "673e7afd971da4c5d03220895ae3a7f1edb30ae891fe7bfdeaf2ce9b8c3224db", "README.md": "9657e19d12463e2fab9284bba975024c93401770d700d04783557c9423105d07", "examples.py": "c03227e13fdf19f1ab13ba8ddc67e90c9f3d3d080908ceecd5997a1a5b3744fa", "memoization/__init__.py": "0f761d59474cdc78abb886d36146a28ac25827046a340acb463aec98b8b70a38", "memoization/backport/__init__.py": "ba44ad61fa5b32c3180eeedfaf401ae016a308f8fa1735a5cb9600ea13d9e9b3", "memoization/backport/backport_enum.py": "a8d6ca7f318775bcafa3fcfd72b52b895d07e647be0da8948ad6a4c1eedae250", "memoization/caching/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/caching/fifo_cache.py": "af4d15801af95c24ed0dcb0df3215cfaf48cef369c84da6f520aec9e374a9680", "memoization/caching/fifo_cache.pyi": "ff4b8e44c934f9dfcf5e353aa30f3a0262d1dd785085a067c9e2bfbb489e2625", "memoization/caching/general/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/caching/general/keys_order_dependent.py": "34435b99bf5e27c008bac93cad9ce7e1732569b33baa685bf7c17dabe07560e6", "memoization/caching/general/keys_order_dependent.pyi": "d7d91e6522ec550dc8a4a2244af747ddc6246dcfd795ec149aa942422a48ace1", "memoization/caching/general/keys_order_independent.py": "337361d05203254237e9d9e5d1a92608ada97cd95424fffafdc28e66cd640757", "memoization/caching/general/keys_order_independent.pyi": "d7d91e6522ec550dc8a4a2244af747ddc6246dcfd795ec149aa942422a48ace1", "memoization/caching/general/values_with_ttl.py": "10d095973e8ddebde1ecebe1a4238363ed7a822dd3889f8cd5af3bf0fbe53aa8", "memoization/caching/general/values_with_ttl.pyi": "411c146a7d5ee3e567b25e83bfa6a78ca577007127088ec03ce462f9e727a935", "memoization/caching/general/values_without_ttl.py": "a18702631510325dea759a13d36286953d9d626c295af129c6a47e8ddad03bfe", "memoization/caching/general/values_without_ttl.pyi": "5f85615cfda56482453558dd496e25fc7fcbaad166907198f21b6abc40cb2e50", "memoization/caching/lfu_cache.py": "d80f67d11e253d42481c1d8b4aed8d54e7eab6d9d67f9b9e4113198cc249dc58", "memoization/caching/lfu_cache.pyi": "ff4b8e44c934f9dfcf5e353aa30f3a0262d1dd785085a067c9e2bfbb489e2625", "memoization/caching/lru_cache.py": "9bbd4e37db7cd26aeb6a61d57685e9183a18470b5a834f1455bc62a74adc3ed1", "memoization/caching/lru_cache.pyi": "ff4b8e44c934f9dfcf5e353aa30f3a0262d1dd785085a067c9e2bfbb489e2625", "memoization/caching/plain_cache.py": "fee838a05cd908d9cbc5fc147fd959640f849152d8fa0c6604bc9324f932bcb4", "memoization/caching/plain_cache.pyi": "ff4b8e44c934f9dfcf5e353aa30f3a0262d1dd785085a067c9e2bfbb489e2625", "memoization/caching/statistic_cache.py": "109457471ddc62f264d6c2de2c3d288a1037b9ba94ddf038ddf890e96cf82ec3", "memoization/caching/statistic_cache.pyi": "ff4b8e44c934f9dfcf5e353aa30f3a0262d1dd785085a067c9e2bfbb489e2625", "memoization/config/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/config/algorithm_mapping.py": "c66e40258a235a026d06e1dab52742564e8a5115b61e202c54a6725037dc8825", "memoization/config/algorithm_mapping.pyi": "68272ea30ae9f3c2e9b3a5ab5ee52805fc6bb3d3dfa5705a551a776f51b4ce3f", "memoization/constant/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/constant/flag.py": "1de1eea12e59a50b36bf92c10034cb2894caa5ad51fabb564fbbb1537983e121", "memoization/constant/flag.pyi": "1948484944836f56c189239bb088b7ee5cc5a958e3f7c9f9c9a20ec8db333af2", "memoization/memoization.py": "3602c2015a0466b9fa67dea6d498787e1fea5f4e2c1d41fb20810ccbdeb6f68c", "memoization/memoization.pyi": "1475d7beb0609962e0cb4af923c8e300c1665f0a5ed51a7a946548ff0a2dee40", "memoization/model.py": "c512785a7de13ede133f4d690c8771b6cd253ac9ecdf7169dc4f34016343f3c6", "memoization/model.pyi": "64540d85c4bacabf829a6320206d02c5ffb673856bc72bb895867e6dbeda75c7", "memoization/py.typed": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/type/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/type/caching/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/type/caching/cache.pyi": "1fb93a11ea729ee0248974f6fd7bdb182641e5f111362a3915d593c0941eb2f3", "memoization/type/caching/general/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/type/caching/general/keys.pyi": "3a706fea380e7d1ecddb25599d3374ef1406afd230ed6decca9ea5ca341f3237", "memoization/type/model.pyi": "ab8add9955d50d01a50e87678f425fe8608619b7abe09fc5429fd37c51f28e14", "memoization/util/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "memoization/util/algorithm_extension_validator.py": "99c5b6565a8ede6fded98f9025d2c6fc84660e87032326131b86905174bfc038", "setup.py": "892654a92dbc1afd4ebdef8a688f2228567b148933cc9c98ab818a3a9e8cfc11", "test.py": "8e66d6da5730b482a330783c919001892d87a71f159310b982711fa88f38da7f"}
JSON

%check
%{__python3} -m pip install --no-index --no-deps --no-compile --target ../memoization-wheel-stage wheelhouse/memoization-0.4.0-*.whl
env -u PYTHONHOME -u PYTHONSTARTUP -u PYTHONPATH -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u COVERAGE_PROCESS_START %{__python3} - "%{buildroot}%{_datadir}/python-memoization/original" "../memoization-wheel-stage" wheel <<'PY'
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
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(p)], text=True).strip() == 'python-memoization'
assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(pathlib.Path(sys.executable).resolve())], text=True).strip() == 'python3'
os.environ['PYTHONPATH'] = str(site)
sys.path[:] = [str(site)] + [p for p in sys.path if p and not pathlib.Path(p).resolve().is_relative_to(original)]
assert importlib.metadata.version('memoization') == '0.4.0'
coverage_module = importlib.import_module('coverage')
coverage_origin = pathlib.Path(coverage_module.__file__).resolve()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(coverage_origin)], text=True).strip() == 'python3-coverage'
coverage_version = importlib.metadata.version('coverage')
assert coverage_version == '7.3.2'
coverage_rpm = subprocess.check_output(['rpm', '-q', '--qf', '%%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}', '--', 'python3-coverage'], text=True).strip()
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
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(p)], text=True).strip() == 'python-memoization'
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
env -u PYTHONHOME -u PYTHONSTARTUP -u PYTHONPATH -u PYTEST_ADDOPTS -u PYTEST_PLUGINS -u COVERAGE_PROCESS_START %{__python3} - "%{buildroot}%{_datadir}/python-memoization/original" "%{buildroot}%{python3_sitelib}" buildroot <<'PY'
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
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(p)], text=True).strip() == 'python-memoization'
assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(pathlib.Path(sys.executable).resolve())], text=True).strip() == 'python3'
os.environ['PYTHONPATH'] = str(site)
sys.path[:] = [str(site)] + [p for p in sys.path if p and not pathlib.Path(p).resolve().is_relative_to(original)]
assert importlib.metadata.version('memoization') == '0.4.0'
coverage_module = importlib.import_module('coverage')
coverage_origin = pathlib.Path(coverage_module.__file__).resolve()
assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(coverage_origin)], text=True).strip() == 'python3-coverage'
coverage_version = importlib.metadata.version('coverage')
assert coverage_version == '7.3.2'
coverage_rpm = subprocess.check_output(['rpm', '-q', '--qf', '%%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}', '--', 'python3-coverage'], text=True).strip()
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
        assert subprocess.check_output(['rpm', '-qf', '--qf', '%%{NAME}', '--', str(p)], text=True).strip() == 'python-memoization'
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

%files
%license LICENSE PYTHON-3.7.2-LICENSE.txt MEMOIZATION-ATTRIBUTION.txt
%doc README.md CONTRIBUTING.md CONTRIBUTORS.md
%{python3_sitelib}/memoization/
%{python3_sitelib}/memoization-0.4.0.dist-info/
%{_datadir}/python-memoization/

%changelog
* Wed Oct 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Preserve full original coverage/unittest route and Python-derived notices.
