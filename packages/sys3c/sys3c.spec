# SPDX-License-Identifier: Apache-2.0
Name:           sys3c
Version:        0.4.0
Release:        1%{?dist}
Summary:        System 1-3 Compiler and Decompiler
License:        GPL-2.0-or-later
URL:            https://github.com/kichikuou/sys3c
Source0:        sys3c-0.4.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
System 1-3 Compiler and Decompiler

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
