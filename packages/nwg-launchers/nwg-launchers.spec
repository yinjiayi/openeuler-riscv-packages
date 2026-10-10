# SPDX-License-Identifier: Apache-2.0
Name:           nwg-launchers
Version:        0.7.1.1
Release:        1%{?dist}
Summary:        GTK+ launchers for sway, i3 and some other WMs
License:        GPL-3.0-or-later
URL:            https://github.com/nwg-piotr/nwg-launchers
Source0:        nwg-launchers-0.7.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
GTK+ launchers for sway, i3 and some other WMs

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
