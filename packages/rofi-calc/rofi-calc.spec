# SPDX-License-Identifier: Apache-2.0
Name:           rofi-calc
Version:        2.5.1
Release:        1%{?dist}
Summary:        Do calculations in rofi
License:        MIT
URL:            https://github.com/svenstaro/rofi-calc
Source0:        rofi-calc-2.5.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Do calculations in rofi

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.1-1
- Initial openEuler RISC-V package from the full package inventory.
