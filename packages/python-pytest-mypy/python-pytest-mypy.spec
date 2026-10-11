# SPDX-License-Identifier: Apache-2.0
Name:           python-pytest-mypy
Version:        1.0.1
Release:        1%{?dist}
Summary:        Mypy static type checker plugin for pytest
License:        MIT
URL:            https://github.com/realpython/pytest-mypy
Source0:        pytest_mypy-1.0.1.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 61
BuildRequires:  python3-setuptools_scm >= 7.1
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-filelock >= 3
BuildRequires:  python3-mypy >= 1
BuildRequires:  python3-pytest >= 7
BuildRequires:  python3-packaging
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-pytest-randomly
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-pexpect
Requires:       python3
Requires:       python3-filelock >= 3
Requires:       python3-mypy >= 1
Requires:       python3-pytest >= 7
Requires:       python3-packaging
Requires:       python3-pytest-cov
Requires:       python3-pytest-randomly
Requires:       python3-pytest-xdist
Requires:       python3-pexpect
BuildArch:      noarch

%description
Pytest-mypy runs the mypy static type checker from pytest. This package retains
the whole original test suite, branch coverage gate, xdist variants and original
upstream skip/xfail markers for source and installed-RPM verification.

%prep
%autosetup -n pytest_mypy-%{version}

%build
export PIP_DISABLE_PIP_VERSION_CHECK=1
python3 -m pip wheel --no-build-isolation --no-deps --no-index --wheel-dir dist .

%install
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} dist/pytest_mypy-%{version}-py3-none-any.whl
install -d %{buildroot}%{_datadir}/%{name}/source/src/pytest_mypy %{buildroot}%{_datadir}/%{name}/source/tests %{buildroot}%{_datadir}/%{name}/source/.github/workflows
install -m 0644 .gitignore CONTRIBUTING.rst LICENSE README.rst changelog.md pyproject.toml tox.ini %{buildroot}%{_datadir}/%{name}/source/
install -m 0644 src/pytest_mypy/__init__.py src/pytest_mypy/py.typed %{buildroot}%{_datadir}/%{name}/source/src/pytest_mypy/
install -m 0644 tests/conftest.py tests/test_pytest_mypy.py %{buildroot}%{_datadir}/%{name}/source/tests/
install -m 0644 .github/workflows/validation.yml .github/workflows/publication.yml %{buildroot}%{_datadir}/%{name}/source/.github/workflows/

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
# The original src layout must not shadow the built wheel. Both outer pytest
# and pytester subprocesses use the installed buildroot distribution/entry point.
export PYTHONPATH=%{buildroot}%{python3_sitelib}
python3 -c 'import pytest_mypy; assert pytest_mypy.__file__.startswith("%{buildroot}%{python3_sitelib}/pytest_mypy/")'
# Outer CLI verbosity only; never inject options into nested pytester processes.
# Persist running/failing node IDs without changing original tests or gates.
# Non-exiting outer worker stack dump; original subprocess args stay unchanged.
pytest -p no:mypy --cov pytest_mypy --cov-branch --cov-fail-under 100 --cov-report term-missing -n auto -vv -rA -o faulthandler_timeout=300

%files
%license LICENSE
%doc README.rst CONTRIBUTING.rst changelog.md
%{python3_sitelib}/pytest_mypy/
%{python3_sitelib}/pytest_mypy-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Pin official stable source and preserve whole original tests and coverage gate.
