# SPDX-License-Identifier: Apache-2.0
Name:           lightning
Version:        2.2.3
Release:        1%{?dist}
Summary:        Library that generates assembly language code at run-time
License:        LGPL-3.0-or-later
URL:            https://www.gnu.org/software/lightning/
Source0:        lightning-2.2.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gcc-c++


%description
Library that generates assembly language code at run-time

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
%license COPYING
%license COPYING.DOC
%license COPYING.LESSER
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.3-1
- Initial openEuler RISC-V package from the full package inventory.
