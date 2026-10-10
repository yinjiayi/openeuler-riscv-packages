# SPDX-License-Identifier: Apache-2.0
Name:           hyprtasking
Version:        0.4
Release:        1%{?dist}
Summary:        Hyprland plugin for workspace overview and management
License:        BSD-3-Clause
URL:            https://github.com/douglas/hyprtasking
Source0:        hyprtasking-0.4.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Hyprland plugin for workspace overview and management

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4-1
- Initial openEuler RISC-V package from the full package inventory.
