# SPDX-License-Identifier: Apache-2.0
Name:           gnudos
Version:        2.0
Release:        1%{?dist}
Summary:        Library designed to help new users of the GNU system, who are coming from a DOS background, fit into the picture and start using the GNU system with ease
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gnudos/
Source0:        gnudos-2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel


%description
Library designed to help new users of the GNU system, who are coming from a DOS background, fit into the picture and start using the GNU system with ease

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0-1
- Initial openEuler RISC-V package from the full package inventory.
