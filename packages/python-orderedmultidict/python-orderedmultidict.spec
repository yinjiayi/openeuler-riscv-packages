# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}
Name:           python-orderedmultidict
Version:        1.0.2
Release:        1%{?dist}
Summary:        Ordered multivalue dictionary for Python
License:        Unlicense
URL:            https://github.com/gruns/orderedmultidict
Source0:        orderedmultidict-1.0.2.tar.gz
Source1:        orderedmultidict-tests-901194bed9c2de9e336358f3328132a81a14314e.tar.gz
BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-six >= 1.8.0
BuildRequires:  python3-flake8
Requires:       python3
Requires:       python3-six >= 1.8.0
Provides:       python3dist(orderedmultidict) = %{version}
Provides:       python3.11dist(orderedmultidict) = %{version}

%description
A multivalue dictionary preserving insertion/deletion order and dict method
parity. Original checks include linked lists, mapping parity, multi-value
update/pop and binary operators.

%prep
%setup -q -n orderedmultidict-%{version}
mkdir upstream-tests
tar -xzf %{SOURCE1} --strip-components=1 -C upstream-tests
# Bind the supplemental tests to this stable release, not an older Git tag.
for file in setup.py MANIFEST.in LICENSE.md orderedmultidict/__init__.py orderedmultidict/__version__.py orderedmultidict/itemlist.py orderedmultidict/orderedmultidict.py; do
    cmp "$file" "upstream-tests/$file"
done
cp -a upstream-tests/tests .
cat > verify-installed.py <<'PY'
import ast
import hashlib
import importlib
import importlib.metadata
import json
import pathlib
import sys
import tempfile
import unittest

assert sys.version_info[:2] == (3, 11) and not sys.flags.optimize
support = pathlib.Path(sys.argv[1]).resolve(strict=True)
site = pathlib.Path(sys.argv[2]).resolve(strict=True)
phase = sys.argv[3]
assert phase in ('staged', 'installed')
runtime = {
    '__init__.py': '3177dca30a17bc6ebbedbaf616bb791087d40beb5760b2a0b581e0b5964a1dce',
    '__version__.py': 'fe5aa2a02e064ef7a328f0095f06376234f2c7eeae04de7c50e6133585f224fa',
    'itemlist.py': '32969d0abd83a457e481370d0ab766f98381983c604ff64635228a665d47f599',
    'orderedmultidict.py': 'd0297f5d49bd5d26ec1fe422fcff49a1477ee48edee7d5f3e8b86b77b6943470',
}
tests = {
    'test_itemlist.py': '042d6377c54f8d8bd4cf4b9d675489ecf580bf00e3ae20cb22311b6d879cab22',
    'test_orderedmultidict.py': 'da035ab2b00867f8600fab7ebeaca0993b5bbdabb684b5cc34d940bd779d8672',
}
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for name, sha in runtime.items():
    p = site / 'orderedmultidict' / name
    assert p.is_file() and not p.is_symlink() and digest(p) == sha
for name, sha in tests.items():
    p = support / 'tests' / name
    assert p.is_file() and not p.is_symlink() and digest(p) == sha
    ast.parse(p.read_text())
assert digest(support / 'LICENSE.md') == '312ba47ef895655fc8f046b3bed4076acc8222ff3f17932b32f88abd76f91deb'
# Only the specified staged or installed runtime wins, never script/cwd paths.
sys.path = [str(site)] + [p for p in sys.path if p and pathlib.Path(p).resolve() not in (support, pathlib.Path.cwd().resolve())]
package = importlib.import_module('orderedmultidict')
assert package.__version__ == '1.0.2'
dist = importlib.metadata.distribution('orderedmultidict')
assert dist.version == '1.0.2' and pathlib.Path(dist.locate_file('')).resolve() == site
for suffix in ('', '.__version__', '.itemlist', '.orderedmultidict'):
    module = importlib.import_module('orderedmultidict' + suffix)
    path = pathlib.Path(module.__file__).resolve(strict=True)
    assert path.parent == site / 'orderedmultidict' and digest(path) == runtime[path.name]
with tempfile.TemporaryDirectory(prefix='orderedmultidict-check-') as fresh:
    root = pathlib.Path(fresh)
    for name in tests:
        (root / name).write_bytes((support / 'tests' / name).read_bytes())
    suite = unittest.TestLoader().discover(str(root))
    assert suite.countTestCases() == 55
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    assert result.wasSuccessful() and result.testsRun == 55 and not result.skipped and not result.expectedFailures and not result.unexpectedSuccesses
for name, sha in runtime.items():
    assert digest(site / 'orderedmultidict' / name) == sha
for name, sha in tests.items():
    assert digest(support / 'tests' / name) == sha
print(json.dumps(dict(phase=phase, tests=55, skipped=0, runtime=str(site / 'orderedmultidict'), original_test_hashes=tests, status='passed'), sort_keys=True))
PY

%build
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1
python3 -m pip wheel --no-deps --no-build-isolation --no-index --wheel-dir dist .
test "$(find dist -name '*.whl' -type f | wc -l)" -eq 1

%install
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1
python3 -m pip install --no-deps --no-index --no-compile --root %{buildroot} --prefix /usr dist/*.whl
install -d %{buildroot}%{_datadir}/%{name}/tests
install -m 0644 tests/test_itemlist.py tests/test_orderedmultidict.py %{buildroot}%{_datadir}/%{name}/tests/
install -m 0644 verify-installed.py LICENSE.md %{buildroot}%{_datadir}/%{name}/

%check
export PIP_NO_INDEX=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1
unset PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONOPTIMIZE
# Upstream's documented complete unittest frontend, unmodified RunTests class.
python3 setup.py test
# Remove the source runtime during staged testing to forbid source fallback.
mv orderedmultidict held-source-runtime
(cd /tmp && python3 -I %{buildroot}%{_datadir}/%{name}/verify-installed.py %{buildroot}%{_datadir}/%{name} %{buildroot}/usr/lib/python3.11/site-packages staged)
mv held-source-runtime orderedmultidict

%files
%license LICENSE.md
%doc README.md API.md
/usr/lib/python3.11/site-packages/orderedmultidict/
/usr/lib/python3.11/site-packages/orderedmultidict-%{version}.dist-info/
%{_datadir}/%{name}/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Pin official stable PyPI release and matching immutable original tests.
- Retain full 55 functional checks and installed RPM provenance, no patch.
