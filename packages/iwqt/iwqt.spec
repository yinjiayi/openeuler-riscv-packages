# SPDX-License-Identifier: Apache-2.0
Name:           iwqt
Version:        0.0.5
Release:        1%{?dist}
Summary:        An iwd network applet for linux systems
License:        GPL-3.0-or-later
URL:            https://github.com/FinGu/iwqt
Source0:        iwqt-0.0.5.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
An iwd network applet for linux systems

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.5-1
- Initial openEuler RISC-V package from the full package inventory.
