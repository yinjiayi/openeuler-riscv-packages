# SPDX-License-Identifier: Apache-2.0
Name:           gslapper
Version:        1.5.2
Release:        1%{?dist}
Summary:        Modern mpvpaper replacement - Wayland wallpaper utility with video/image support and instant switching via RAM cache
License:        GPL-3.0-or-later
URL:            https://github.com/Nomadcxx/gSlapper
Source0:        gslapper-1.5.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Modern mpvpaper replacement - Wayland wallpaper utility with video/image support and instant switching via RAM cache

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.2-1
- Initial openEuler RISC-V package from the full package inventory.
