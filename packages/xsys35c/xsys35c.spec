# SPDX-License-Identifier: Apache-2.0
Name:           xsys35c
Version:        1.13.0
Release:        1%{?dist}
Summary:        System 3.x Compiler and Decompiler
License:        GPL-2.0-or-later
URL:            https://github.com/kichikuou/xsys35c
Source0:        xsys35c-1.13.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
System 3.x Compiler and Decompiler

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13.0-1
- Initial openEuler RISC-V package from the full package inventory.
