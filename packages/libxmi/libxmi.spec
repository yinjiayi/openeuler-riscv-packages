# SPDX-License-Identifier: Apache-2.0
Name:           libxmi
Version:        1.2
Release:        1%{?dist}
Summary:        A library for rasterizing 2-D vector graphics
License:        GPL-2.0-or-later
URL:            https://www.gnu.org/software/libxmi/
Source0:        libxmi-1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make


%description
A library for rasterizing 2-D vector graphics

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2-1
- Initial openEuler RISC-V package from the full package inventory.
