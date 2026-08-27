# SPDX-License-Identifier: Apache-2.0
Name:           wlsbg
Version:        3.3.7
Release:        4%{?dist}
Summary:        Wallpaper tool with shader support for Wayland compositors
License:        MIT
URL:            https://github.com/Sublimeful/wlsbg
Source0:        wlsbg-3.3.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel

%description
Wallpaper tool with shader support for Wayland compositors

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
%license LICENSE.txt
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.7-4
- Add the OpenGL development files required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.7-3
- Add the Wayland protocols development data required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.7-2
- Add the Wayland EGL development dependency required by Meson.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.7-1
- Initial openEuler RISC-V package from the full package inventory.
