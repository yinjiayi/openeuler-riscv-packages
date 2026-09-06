# SPDX-License-Identifier: Apache-2.0
Name:           swbis
Version:        1.13.3
Release:        1%{?dist}
Summary:        software packaging -- again
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/swbis/
Source0:        swbis-1.13.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gettext-devel
BuildRequires:  man-db
BuildRequires:  rpm-devel
BuildRequires:  zlib-devel


%description
software packaging -- again

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13.3-1
- Initial openEuler RISC-V package from the full package inventory.
