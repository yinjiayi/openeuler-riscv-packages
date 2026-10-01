# SPDX-License-Identifier: Apache-2.0
Name:           flawfinder
Version:        2.0.20
Release:        1%{?dist}
Summary:        Lexical scanner for security flaws in C and C++ source
License:        GPL-2.0-or-later
URL:            https://dwheeler.com/flawfinder/
Source0:        flawfinder-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-setuptools
Requires:       python3

%description
Flawfinder examines C and C++ source code and reports lexical patterns that
may indicate security weaknesses, ranked by severity and mapped to CWE IDs.

%prep
%autosetup -p1

%build
python3 -m py_compile flawfinder.py

%install
%make_install prefix=%{_prefix}

%check
%make_build test PYTHON=python3

%files
%license COPYING
%doc ChangeLog README.md
%{_bindir}/flawfinder
%{_mandir}/man1/flawfinder.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.20-1
- Initial openEuler RISC-V Flawfinder package with complete upstream tests.
