# SPDX-License-Identifier: Apache-2.0
Name:           wob
Version:        0.16
Release:        1%{?dist}
Summary:        A lightweight overlay volume/backlight/progress/anything bar for Wayland
License:        ISC
URL:            https://github.com/francma/wob
Source0:        wob-0.16.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A lightweight overlay volume/backlight/progress/anything bar for Wayland

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16-1
- Initial openEuler RISC-V package from the full package inventory.
