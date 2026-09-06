# SPDX-License-Identifier: Apache-2.0
Name:           wljoywake
Version:        0.3
Release:        1%{?dist}
Summary:        Wayland idle inhibit on joystick input
License:        GPL-2.0-or-later
URL:            https://github.com/nowrep/wljoywake
Source0:        wljoywake-0.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Wayland idle inhibit on joystick input

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3-1
- Initial openEuler RISC-V package from the full package inventory.
