# SPDX-License-Identifier: Apache-2.0
Name:           python-case-converter
Version:        1.2.0
Release:        1%{?dist}
Summary:        Python string case conversion library
License:        MIT
URL:            https://github.com/chrisdoherty4/python-case-converter
Source0:        case-converter-1.2.0.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 40.8.0
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-build >= 1.0.3
BuildRequires:  python3-pyproject-hooks
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-coverage
BuildRequires:  make
BuildRequires:  python-pip-wheel = 23.3.1
BuildRequires:  python-setuptools = 68.0.0
BuildRequires:  python-wheel-wheel = 1:0.40.0
Requires:       python3
Requires:       python3-pip
Requires:       python3-build >= 1.0.3
Requires:       python3-pyproject-hooks
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-coverage
Requires:       make
Requires:       python-pip-wheel = 23.3.1
Requires:       python-setuptools = 68.0.0
Requires:       python-wheel-wheel = 1:0.40.0
BuildArch:      noarch

%description
Case-converter converts strings between camel, Pascal, snake, kebab, macro,
COBOL, flat and title cases. The complete original test suite and isolated
source-distribution-to-wheel build are retained for offline target CI.

%prep
%autosetup -n python-case-converter-c37a1240f08b0f8ec1963910fdfda23b51f013a1

%build
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH
export PIP_NO_INDEX=1 PIP_FIND_LINKS=/usr/share/python-wheels
export PIP_CONFIG_FILE=/dev/null PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
# Preserve the unmodified upstream default, including PEP 517 build isolation.
# Target ensurepip and the fixed official seed-wheel RPMs supply bootstrap
# pip/setuptools; isolated backend requirements resolve from the same wheelhouse.
make package

%install
python3 -m pip install --no-index --no-deps --no-compile --root %{buildroot} --prefix %{_prefix} dist/case_converter-%{version}-py3-none-any.whl
# Retain exactly the 28 original Git blobs, not generated dist/build/egg-info.
install -d %{buildroot}%{_datadir}/%{name}/source/caseconverter %{buildroot}%{_datadir}/%{name}/source/.vscode
install -m 0644 .gitignore .gitlab-ci.yml LICENSE Makefile README.md setup.py %{buildroot}%{_datadir}/%{name}/source/
install -m 0644 .vscode/launch.json .vscode/settings.json %{buildroot}%{_datadir}/%{name}/source/.vscode/
install -m 0644 caseconverter/*.py %{buildroot}%{_datadir}/%{name}/source/caseconverter/

%check
export PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1
unset PYTHONPATH
# Original full nine-module glob and coverage invocation, without selectors.
make coverage

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/caseconverter/
%{python3_sitelib}/case_converter-*.dist-info/
%{_datadir}/%{name}/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Pin the complete official release tree and preserve whole upstream defaults offline.
