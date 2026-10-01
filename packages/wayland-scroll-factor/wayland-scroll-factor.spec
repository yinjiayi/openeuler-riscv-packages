# SPDX-License-Identifier: Apache-2.0
Name:           wayland-scroll-factor
Version:        1.0.0
Release:        1%{?dist}
Summary:        Touchpad scroll and gesture tuning for Wayland (GNOME)
License:        MIT
URL:            https://github.com/daniel-g-carrasco/wayland-scroll-factor
Source0:        wayland-scroll-factor-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Touchpad scroll and gesture tuning for Wayland (GNOME)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
