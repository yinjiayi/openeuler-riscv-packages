# SPDX-License-Identifier: Apache-2.0
Name:           python-titlecase
Version:        2.4.1
Release:        1%{?dist}
Summary:        English title capitalization with abbreviation heuristics
License:        MIT
URL:            https://github.com/ppannuto/python-titlecase
Source0:        titlecase-2.4.1.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 46.1.0
BuildRequires:  python3-setuptools_scm >= 5
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-regex >= 2020.4.4
BuildRequires:  python3-coverage
Requires:       python3
Requires:       python3-regex >= 2020.4.4
Requires:       python3-coverage
BuildArch:      noarch

%description
Titlecase applies English title capitalization and abbreviation heuristics.
The whole original unittest suite is retained, with both regex and standard
library re engines. Original upstream skips remain visible and unchanged.

%prep
%autosetup -n python-titlecase-418c57ca6c7f324ddc2813b3fc88d52e84db63bd

%build
export PIP_DISABLE_PIP_VERSION_CHECK=1
# Official release Git archive has no .git directory; SCM receives the
# verified release-tag version without modifying any original configuration.
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
python3 -m pip wheel --no-build-isolation --no-deps --no-index --wheel-dir dist .

%install
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} dist/titlecase-%{version}-py2.py3-none-any.whl
install -d %{buildroot}%{_datadir}/%{name}/source/titlecase %{buildroot}%{_datadir}/%{name}/source/.github/workflows
install -m 0644 .gitignore AUTHORS.rst LICENSE.txt README.rst pyproject.toml setup.cfg setup.py tox.ini %{buildroot}%{_datadir}/%{name}/source/
install -m 0644 titlecase/__init__.py titlecase/tests.py %{buildroot}%{_datadir}/%{name}/source/titlecase/
install -m 0644 .github/workflows/ci.yml .github/workflows/coverage.yml %{buildroot}%{_datadir}/%{name}/source/.github/workflows/

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH
check_root=$(mktemp -d)
trap 'rm -rf -- "$check_root"' EXIT
mkdir "$check_root/no-regex" "$check_root/bin"
# openEuler names the original coverage entry point coverage3. Keep the
# upstream command unchanged with an isolated alias to that exact provider.
ln -s /usr/bin/coverage3 "$check_root/bin/coverage"
export PATH="$check_root/bin:$PATH"
cat > "$check_root/no-regex/sitecustomize.py" <<'PY'
import sys
class NoOptionalRegex:
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'regex' or fullname.startswith('regex.'):
            raise ModuleNotFoundError('optional regex intentionally absent')
sys.meta_path.insert(0, NoOptionalRegex())
PY
python3 -c 'import titlecase; assert titlecase.REGEX_AVAILABLE is True'
python3 -m unittest
COVERAGE_FILE="$check_root/coverage-regex" coverage run -m unittest
PYTHONPATH="$check_root/no-regex" python3 -c 'import titlecase; assert titlecase.REGEX_AVAILABLE is False'
PYTHONPATH="$check_root/no-regex" python3 -m unittest
PYTHONPATH="$check_root/no-regex" COVERAGE_FILE="$check_root/coverage-re" coverage run -m unittest

%files
%license LICENSE.txt
%doc README.rst AUTHORS.rst
%{_bindir}/titlecase
%{python3_sitelib}/titlecase/
%{python3_sitelib}/titlecase-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-1
- Pin the official stable release tree and retain both whole default test engines.
