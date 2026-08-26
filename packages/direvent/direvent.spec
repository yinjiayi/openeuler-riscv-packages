# SPDX-License-Identifier: Apache-2.0
Name:           direvent
Version:        5.5
Release:        1%{?dist}
Summary:        Deamon that monitors events in the file system directories
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/direvent/
Source0:        direvent-5.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel


%description
Deamon that monitors events in the file system directories

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.5-1
- Initial openEuler RISC-V package from the full package inventory.
