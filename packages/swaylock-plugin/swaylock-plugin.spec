# SPDX-License-Identifier: Apache-2.0
Name:           swaylock-plugin
Version:        1.8.7
Release:        1%{?dist}
Summary:        A fork of the swaylock screen locker for Wayland supporting custom wallpaper drawing programs
License:        MIT
URL:            https://github.com/mstoeckl/swaylock-plugin
Source0:        swaylock-plugin-1.8.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A fork of the swaylock screen locker for Wayland supporting custom wallpaper drawing programs

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.7-1
- Initial openEuler RISC-V package from the full package inventory.
