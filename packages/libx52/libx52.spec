# SPDX-License-Identifier: Apache-2.0
Name:           libx52
Version:        0.3.3
Release:        1%{?dist}
Summary:        Application to control the MFD and LEDs of a Saitek X52/X52Pro HOTAS
License:        GPL-2.0-or-later
URL:            https://github.com/nirenjan/libx52
Source0:        libx52-0.3.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Application to control the MFD and LEDs of a Saitek X52/X52Pro HOTAS

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.3-1
- Initial openEuler RISC-V package from the full package inventory.
