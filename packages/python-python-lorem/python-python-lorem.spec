# SPDX-License-Identifier: Apache-2.0
Name:           python-python-lorem
Version:        1.3.0.post3
Release:        1%{?dist}
Summary:        Pythonic lorem ipsum generator
License:        BSD-3-Clause
URL:            https://jarryshaw.github.io/lorem/
Source0:        lorem-1.3.0.post3-fixed.tar.gz
Patch0:         0001-compatible-bdist-wheel-import.patch
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools >= 61
BuildRequires:  python3-wheel
BuildRequires:  python3-coverage

%description
Pythonic lorem ipsum generator

%package -n python3-python-lorem
Summary:        %{summary}
Requires:       python3
Requires:       python3-coverage
Provides:       python-python-lorem = %{version}-%{release}

%description -n python3-python-lorem
Pythonic lorem ipsum generator.

%prep
%autosetup -n lorem-04b9e25393906e45e1894b1c63a62e0224a370c7 -p1

%build
%py3_build

%install
%py3_install
install -Dpm 0644 .coveragerc %{buildroot}%{_datadir}/python-python-lorem/tests/.coveragerc

%check
# Full unchanged upstream Python 3.11 workflow suite and coverage configuration.
# The target console name is python3-coverage; this is the same module entry.
%{__python3} -m coverage run test_lorem.py

%files -n python3-python-lorem
%license LICENSE
%doc README.md
%{python3_sitelib}/lorem.py
%{python3_sitelib}/test_lorem.py
%{python3_sitelib}/__pycache__/lorem*.pyc
%{python3_sitelib}/__pycache__/test_lorem*.pyc
%{python3_sitelib}/python_lorem-*.egg-info/
%{_datadir}/python-python-lorem/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0.post3-1
- Initial package retaining the full original coverage and unittest contract.
- Use wheel's compatible build command only when the setuptools module is absent.
