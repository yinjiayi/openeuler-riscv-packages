# SPDX-License-Identifier: Apache-2.0
Name:           xdg-desktop-portal-adw
Version:        1.0.2
Release:        1%{?dist}
Summary:        A backend implementation for xdg-desktop-portal using Libadwaita
License:        LGPL-2.1-or-later
URL:            https://github.com/PrincParshia/xdg-desktop-portal-adw
Source0:        xdg-desktop-portal-adw-1.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A backend implementation for xdg-desktop-portal using Libadwaita

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
