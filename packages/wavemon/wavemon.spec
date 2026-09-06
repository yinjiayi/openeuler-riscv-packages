# SPDX-License-Identifier: Apache-2.0
Name:           wavemon
Version:        0.9.7
Release:        1%{?dist}
Summary:        Ncurses-based monitoring application for wireless network devices
License:        GPL-3.0-or-later
URL:            https://github.com/uoaerg/wavemon
Source0:        wavemon-0.9.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Ncurses-based monitoring application for wireless network devices

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.7-1
- Initial openEuler RISC-V package from the full package inventory.
