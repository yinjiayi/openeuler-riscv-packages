# SPDX-License-Identifier: Apache-2.0
Name:           x86-simd-sort
Version:        7.0
Release:        1%{?dist}
Summary:        C++ template library for high performance SIMD based sorting algorithms
License:        BSD-3-Clause
URL:            https://github.com/intel/x86-simd-sort
Source0:        x86-simd-sort-7.0.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
C++ template library for high performance SIMD based sorting algorithms

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
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0-1
- Initial openEuler RISC-V package from the full package inventory.
