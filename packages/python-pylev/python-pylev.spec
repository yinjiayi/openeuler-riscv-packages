# SPDX-License-Identifier: Apache-2.0
Name:           python-pylev
Version:        1.4.0
Release:        1%{?dist}
Summary:        Pure Python Levenshtein distance implementation
License:        BSD-3-Clause
URL:            https://github.com/toastdriven/pylev
Source0:        pylev-1.4.0.tar.gz
Source1:        pylev-1.4.0-tests.py
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

%description
Pure Python implementations of Levenshtein and Damerau-Levenshtein distance.

%package -n python3-pylev
Summary:        %{summary}
Requires:       python3
Provides:       python-pylev = %{version}-%{release}

%description -n python3-pylev
Pure Python implementations of Levenshtein and Damerau-Levenshtein distance.

%prep
%autosetup -n pylev-%{version} -p1
# PyPI omits tests; this is the entire unchanged test file from the release tag.
cp -p %{SOURCE1} tests.py

%build
%py3_build

%install
%py3_install
install -Dpm 0644 tests.py %{buildroot}%{_datadir}/python-pylev/tests/tests.py

%check
# Exact upstream Travis default: all 22 original unittest cases, unchanged.
%{__python3} tests.py

%files -n python3-pylev
%license LICENSE
%doc README.rst
%{python3_sitelib}/pylev/
%{python3_sitelib}/pylev-*.egg-info/
%{_datadir}/python-pylev/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.0-1
- Initial package retaining the complete original release-tag test suite.
