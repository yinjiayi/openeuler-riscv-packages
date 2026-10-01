# SPDX-License-Identifier: Apache-2.0
Name:           xdg-desktop-portal-xapp-filepicker
Version:        1.1.4
Release:        1%{?dist}
Summary:        A backend implementation for xdg-desktop-portal using GTK/Cinnamon with native folder selection support
License:        LGPL-2.1-or-later
URL:            https://github.com/Twilight0/xdg-desktop-portal-xapp-filepicker
Source0:        xdg-desktop-portal-xapp-filepicker-1.1.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A backend implementation for xdg-desktop-portal using GTK/Cinnamon with native folder selection support

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
