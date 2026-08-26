# SPDX-License-Identifier: Apache-2.0
Name:           rush
Version:        2.4
Release:        1%{?dist}
Summary:        GNU Restricted User Shell
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/rush/
Source0:        rush-2.4.tar.xz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel


%description
GNU Restricted User Shell

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4-1
- Initial openEuler RISC-V package from the full package inventory.
