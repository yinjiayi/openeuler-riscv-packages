# SPDX-License-Identifier: Apache-2.0
Name:           jgmenu
Version:        4.5.0
Release:        1%{?dist}
Summary:        Simple, independent, contemporary-looking X11 menu, designed for scripting, ricing and tweaking
License:        GPL-2.0-or-later
URL:            https://github.com/johanmalm/jgmenu
Source0:        jgmenu-4.5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Simple, independent, contemporary-looking X11 menu, designed for scripting, ricing and tweaking

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
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
