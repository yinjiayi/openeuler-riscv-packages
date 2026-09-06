# SPDX-License-Identifier: Apache-2.0
Name:           rcs
Version:        5.10.1
Release:        1%{?dist}
Summary:        Revision Control System: manages multiple revisions of files
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/rcs/
Source0:        rcs-5.10.1.tar.lz
BuildRequires:  gcc
BuildRequires:  lzip
BuildRequires:  make
BuildRequires:  ed


%description
Revision Control System: manages multiple revisions of files

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.10.1-1
- Initial openEuler RISC-V package from the full package inventory.
