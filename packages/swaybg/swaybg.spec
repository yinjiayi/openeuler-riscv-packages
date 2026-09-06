# SPDX-License-Identifier: Apache-2.0
Name:           swaybg
Version:        1.2.2
Release:        1%{?dist}
Summary:        Wallpaper tool for Wayland compositors
License:        MIT
URL:            https://github.com/swaywm/swaybg
Source0:        swaybg-1.2.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Wallpaper tool for Wayland compositors

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.2-1
- Initial openEuler RISC-V package from the full package inventory.
