# SPDX-License-Identifier: Apache-2.0
Name:           python-pyluach
Version:        2.3.0
Release:        1%{?dist}
Summary:        Hebrew calendar dates and Hebrew Gregorian conversion for Python
License:        MIT
URL:            https://github.com/simlist/pyluach
Source0:        pyluach-2.3.0.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel >= 3.8
BuildRequires:  python3-flit-core >= 3.2
BuildRequires:  python3-flit-core < 4
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-pytest >= 6.0
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-beautifulsoup4
BuildRequires:  python3-flake8
%description
Pyluach provides Hebrew and Gregorian calendar conversions, date arithmetic,
weekly readings, holidays and text or HTML Hebrew calendars.

%package -n python3-pyluach
Summary:        Hebrew calendar dates and Hebrew Gregorian conversion for Python
Provides:       python-pyluach = %{version}-%{release}

%description -n python3-pyluach
Python 3 modules for Hebrew and Gregorian calendar conversions, date
arithmetic, weekly readings, holidays and text or HTML Hebrew calendars.

%prep
%autosetup -p1 -n pyluach-c1ffe4265f25ab7f5d850f4720111470f27e7ce5

%build
# Preserve the original flit_core backend. All dependencies are target RPMs.
%{__python3} -m pip wheel --no-deps --no-build-isolation --no-index --wheel-dir dist .

%install
%{__python3} -m pip install --no-deps --no-index --ignore-installed --no-compile --root %{buildroot} --prefix %{_prefix} dist/pyluach-%{version}-*.whl

%check
# Original CI runs this complete suite with coverage and BeautifulSoup.
# PYTHONPATH supplies the same unchanged src package as upstream's editable install.
PYTHONPATH=src %{__python3} -m pytest --cov=src/pyluach tests/

%files -n python3-pyluach
%license license.txt
%doc README.rst CHANGELOG.rst
%{python3_sitelib}/pyluach/
%{python3_sitelib}/pyluach-%{version}.dist-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Onboard official immutable source and retain the complete MIT license.
- Preserve the original flit backend and all default pytest coverage tests.
