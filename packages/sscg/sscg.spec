# SPDX-License-Identifier: Apache-2.0
Name:           sscg
Version:        4.0.3
Release:        1%{?dist}
Summary:        Simple Signed Certificate Generator
License:        GPL-3.0-or-later
URL:            https://github.com/sgallagher/sscg
Source0:        sscg-4.0.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Simple Signed Certificate Generator

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
