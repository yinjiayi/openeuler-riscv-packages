# SPDX-License-Identifier: Apache-2.0
Name:           gnushogi
Version:        1.4.2
Release:        1%{?dist}
Summary:        GNU gnushogi package
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gnushogi/
Source0:        gnushogi-1.4.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel


%description
GNU gnushogi package

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-1
- Initial openEuler RISC-V package from the full package inventory.
