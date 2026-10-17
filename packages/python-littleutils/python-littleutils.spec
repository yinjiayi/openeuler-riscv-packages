# SPDX-License-Identifier: Apache-2.0
Name:           python-littleutils
Version:        0.2.4
Release:        1%{?dist}
Summary:        Small collection of Python utility functions
License:        MIT AND PSF-2.0
URL:            https://github.com/alexmojaki/littleutils
Source0:        littleutils-0.2.4.tar.gz
Source1:        LICENSE.cpython

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-wheel

%description
Littleutils provides small utility functions for containers, exception
reporting, logging, JSON encoding, grouping and string handling.

%package -n python3-littleutils
Summary:        Small collection of Python utility functions
Provides:       python-littleutils = %{version}-%{release}
Obsoletes:      python-littleutils < %{version}-%{release}

%description -n python3-littleutils
Littleutils utility functions installed for Python 3.

%prep
%autosetup -p1 -n littleutils-5e548dd0af1c1548f08baae5e01dc464d642cbf3
cp -p %{SOURCE1} LICENSE.cpython

%build
# A commit archive has no .git; retain the upstream setuptools_scm backend
# and bind its supported override to the independently verified v0.2.4 tag.
SETUPTOOLS_SCM_PRETEND_VERSION=%{version} %py3_build

%install
SETUPTOOLS_SCM_PRETEND_VERSION=%{version} %py3_install

%check
# Exact default command from upstream tox.ini and GitHub test.yml: all
# embedded doctests run, including their original expected exceptions.
%{__python3} littleutils/__init__.py

%files -n python3-littleutils
%license LICENSE LICENSE.cpython
%{python3_sitelib}/littleutils/
%{python3_sitelib}/littleutils-%{version}-py*.egg-info/

%changelog
* Sat Oct 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.4-1
- Manage the official upstream update from target 0.2.2 to 0.2.4.
- Preserve the complete upstream doctest driver and PSF-derived notice.
