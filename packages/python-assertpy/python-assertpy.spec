# SPDX-License-Identifier: Apache-2.0
%global upstream_commit b9ad7ee2d673a45f9a5b68c3b7aa2d077560bb7c
Name:           python-assertpy
Version:        2.35.0
Release:        1%{?dist}
Summary:        Fluent assertion library for Python unit testing
License:        BSD-3-Clause
URL:            https://github.com/assertpy/assertpy
Source0:        v2.35.0
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-requests

%description
A fluent assertion library for Python unit tests. The complete unchanged
upstream suite and coverage command are retained for target acceptance.

%package -n python3-assertpy
Summary:        %{summary}
Provides:       python-assertpy = %{version}-%{release}
Requires:       python3
Requires:       python3-pytest
Requires:       python3-pytest-cov
Requires:       python3-requests

%description -n python3-assertpy
The Python 3 library and RPM-owned original test suite. Pytest-cov and requests
are installed test support, not upstream library runtime dependencies.

%prep
%autosetup -n assertpy-%{upstream_commit}

%build
%py3_build

%install
%py3_install
mkdir -p %{buildroot}%{_datadir}/python-assertpy/tests
cp -a tests %{buildroot}%{_datadir}/python-assertpy/tests/
install -m 0644 setup.cfg %{buildroot}%{_datadir}/python-assertpy/tests/setup.cfg
install -m 0644 .coveragerc %{buildroot}%{_datadir}/python-assertpy/tests/.coveragerc
install -m 0644 .travis.yml %{buildroot}%{_datadir}/python-assertpy/tests/upstream-travis.yml

%check
# Fail before the unchanged suite if its optional requests case would be absent.
python3 -c 'import requests, pytest_cov.plugin; assert callable(requests.structures.CaseInsensitiveDict)'
PYTHONPATH=. python3 -m pytest -v --cov=assertpy --cov-report term-missing tests

%files -n python3-assertpy
%license LICENSE
%doc README.md
%{python3_sitelib}/assertpy/
%{python3_sitelib}/assertpy-*.egg-info/
%{_datadir}/python-assertpy/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Package official fixed stable release and full original coverage test suite.
