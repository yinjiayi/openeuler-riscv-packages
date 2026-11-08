# SPDX-License-Identifier: Apache-2.0
Name:           cgicc
Version:        3.2.20
Release:        1%{?dist}
Summary:        C++ library that simplifies the creation of CGI applications
License:        LGPL-3.0-or-later AND GFDL-1.2-or-later
URL:            https://www.gnu.org/software/cgicc/
Source0:        cgicc-3.2.20.tar.gz
BuildRequires:  autoconf
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gcc-c++


%description
C++ library that simplifies the creation of CGI applications

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING.DOC
%license COPYING.LIB
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.20-1
- Initial openEuler RISC-V package from the full package inventory.
