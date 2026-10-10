# SPDX-License-Identifier: Apache-2.0
Name:           g2
Version:        0.72
Release:        1%{?dist}
Summary:        2D graphics library; can be used with C, C++, Fortran to generate flow charts.
License:        LGPL-2.1-or-later
URL:            https://github.com/danielrmeyer/g2
Source0:        g2-0.72.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
2D graphics library; can be used with C, C++, Fortran to generate flow charts.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.72-1
- Initial openEuler RISC-V package from the full package inventory.
