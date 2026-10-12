# SPDX-License-Identifier: Apache-2.0
Name:           ddrescue
Version:        1.30
Release:        1%{?dist}
Summary:        GNU data recovery tool
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/ddrescue/
Source0:        ddrescue-1.30.tar.lz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  lzip
BuildRequires:  make


%description
GNU data recovery tool

%prep
%autosetup -p1

%build
%configure
%make_build CXXFLAGS="%{optflags}"

%install
%make_install

%check
%make_build check

%files
%license COPYING
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.30-1
- Initial openEuler RISC-V package from the full package inventory.
