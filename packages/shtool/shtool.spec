# SPDX-License-Identifier: Apache-2.0
Name:           shtool
Version:        2.0.8
Release:        1%{?dist}
Summary:        GNU shtool package
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/shtool/
Source0:        shtool-2.0.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
GNU shtool package

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
%doc AUTHORS
%doc ChangeLog
%doc NEWS
%doc README
%{_bindir}/*

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.8-1
- Initial openEuler RISC-V package from the full package inventory.
