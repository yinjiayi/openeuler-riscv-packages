# SPDX-License-Identifier: Apache-2.0
Name:           python-six
Version:        1.17.0
Release:        1%{?dist}
Summary:        Python compatibility utilities for Python 2 and 3 code
License:        MIT
URL:            https://github.com/benjaminp/six
Source0:        six-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-tkinter

%description
Six provides small utilities that smooth differences between Python 2 and
Python 3 APIs, types, metaclasses, exceptions, and renamed modules.

%package -n python3-six
Summary:        Python 3 compatibility utilities from Six

%description -n python3-six
Six compatibility utilities installed for Python 3.

%prep
%autosetup -p1 -n six-ebd9b3af90247b8858d415a05e96e9ee61e48d07

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pytest -v

%files -n python3-six
%license LICENSE
%doc CHANGES README.rst documentation/index.rst
%{python3_sitelib}/six.py
%{python3_sitelib}/__pycache__/six.*
%{python3_sitelib}/six-%{version}-py*.egg-info

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.17.0-1
- Update the target package with the complete upstream pytest suite.
