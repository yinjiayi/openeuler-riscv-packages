# SPDX-License-Identifier: Apache-2.0
Name:           gnurobots
Version:        1.2.0
Release:        1%{?dist}
Summary:        A robot programming game
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gnurobots/
Source0:        gnurobots-1.2.0.tar.gz
BuildRequires:  gcc
BuildRequires:  guile-devel
BuildRequires:  make
BuildRequires:  glib2-devel
BuildRequires:  ncurses-devel
BuildRequires:  gtk2-devel


%description
A robot programming game

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
