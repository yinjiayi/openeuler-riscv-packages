# SPDX-License-Identifier: Apache-2.0
Name:           gnugo
Version:        3.8
Release:        1%{?dist}
Summary:        Program that plays the game of Go
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gnugo/
Source0:        gnugo-3.8.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
Program that plays the game of Go

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8-1
- Initial openEuler RISC-V package from the full package inventory.
