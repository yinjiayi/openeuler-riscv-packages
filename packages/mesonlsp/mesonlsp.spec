# SPDX-License-Identifier: Apache-2.0
Name:           mesonlsp
Version:        5.0.3
Release:        1%{?dist}
Summary:        Meson language server
License:        GPL-3.0-or-later
URL:            https://github.com/JCWasmx86/mesonlsp
Source0:        mesonlsp-5.0.3.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Meson language server

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
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
