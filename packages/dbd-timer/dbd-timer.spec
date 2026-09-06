# SPDX-License-Identifier: Apache-2.0
Name:           dbd-timer
Version:        1.0.2
Release:        1%{?dist}
Summary:        Overlay stopwatch with two independent timers, Wayland overlay, and gamepad support
License:        MIT
URL:            https://github.com/tkmxqrdxddd/dbd-1v1-timer-linux
Source0:        dbd-timer-1.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Overlay stopwatch with two independent timers, Wayland overlay, and gamepad support

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
