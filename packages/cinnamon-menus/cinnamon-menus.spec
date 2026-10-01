# SPDX-License-Identifier: Apache-2.0
Name:           cinnamon-menus
Version:        6.6.0
Release:        1%{?dist}
Summary:        The cinnamon-menu library
License:        GPL-2.0-or-later
URL:            https://github.com/linuxmint/cinnamon-menus
Source0:        cinnamon-menus-6.6.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
The cinnamon-menu library

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%license COPYING.LIB
%doc README
%doc NEWS
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
