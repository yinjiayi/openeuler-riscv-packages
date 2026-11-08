# SPDX-License-Identifier: Apache-2.0
Name:           fontopia
Version:        1.8.4
Release:        1%{?dist}
Summary:        Text-based vt font editor
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/fontopia/
Source0:        fontopia-1.8.4.tar.gz
BuildRequires:  gcc
BuildRequires:  gnudos-devel
BuildRequires:  make
BuildRequires:  ncurses-devel


%description
Text-based vt font editor

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.4-1
- Initial openEuler RISC-V package from the full package inventory.
