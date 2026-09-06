# SPDX-License-Identifier: Apache-2.0
Name:           still
Version:        0.0.9
Release:        1%{?dist}
Summary:        Freeze the screen of a Wayland compositor until a provided command exits
License:        MIT
URL:            https://github.com/faergeek/still
Source0:        still-0.0.9.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Freeze the screen of a Wayland compositor until a provided command exits

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.9-1
- Initial openEuler RISC-V package from the full package inventory.
