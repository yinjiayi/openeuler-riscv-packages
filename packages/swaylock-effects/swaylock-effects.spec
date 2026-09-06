# SPDX-License-Identifier: Apache-2.0
Name:           swaylock-effects
Version:        1.7.0.0
Release:        1%{?dist}
Summary:        A fancier screen locker for Wayland.
License:        MIT
URL:            https://github.com/jirutka/swaylock-effects
Source0:        swaylock-effects-1.7.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A fancier screen locker for Wayland.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
