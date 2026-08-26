# SPDX-License-Identifier: Apache-2.0
Name:           sharutils
Version:        4.15.2
Release:        1%{?dist}
Summary:        Makes so-called shell archives out of many files
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/sharutils/
Source0:        sharutils-4.15.2.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel


%description
Makes so-called shell archives out of many files

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.15.2-1
- Initial openEuler RISC-V package from the full package inventory.
