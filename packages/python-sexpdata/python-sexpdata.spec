# SPDX-License-Identifier: Apache-2.0
Name:           python-sexpdata
Version:        1.0.2
Release:        1%{?dist}
Summary:        S-expression parser and serializer for Python
License:        BSD-2-Clause
URL:            https://github.com/jd-boyd/sexpdata
Source0:        sexpdata-1.0.2-fixed.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest

%description
S-expression parser and serializer for Python.

%package -n python3-sexpdata
Summary:        %{summary}
Requires:       python3
Requires:       python3-pytest
Provides:       python-sexpdata = %{version}-%{release}

%description -n python3-sexpdata
S-expression parser and serializer for Python.

%prep
%autosetup -n sexpdata-29170a5daed7c07a8d035856356416141210d963 -p1

%build
%py3_build

%install
%py3_install
install -Dpm 0644 test_sexpdata.py %{buildroot}%{_datadir}/python-sexpdata/tests/test_sexpdata.py

%check
# Complete unchanged current upstream Python 3.11 workflow suite.
%{__python3} -m pytest --doctest-modules sexpdata.py test_sexpdata.py

%files -n python3-sexpdata
# LICENSE carries 2019 BSD2; unchanged full module reproduces 2012 BSD2 notice.
%license LICENSE sexpdata.py
%doc README.rst
%{python3_sitelib}/sexpdata.py
%{python3_sitelib}/__pycache__/sexpdata*.pyc
%{python3_sitelib}/sexpdata-*.egg-info/
%{_datadir}/python-sexpdata/

%changelog
* Sun Oct 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial package retaining complete upstream pytest and module doctests.
