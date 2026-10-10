# SPDX-License-Identifier: Apache-2.0
Name:           rdm
Version:        1.4.1
Release:        1%{?dist}
Summary:        A simple yet powerful dotfile manager powered by lua
License:        GPL-3.0-or-later
URL:            https://github.com/Rikaisan/rdm
Source0:        rdm-1.4.1.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A simple yet powerful dotfile manager powered by lua

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
