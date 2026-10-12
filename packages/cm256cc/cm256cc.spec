# SPDX-License-Identifier: Apache-2.0
Name:           cm256cc
Version:        1.1.2
Release:        1%{?dist}
Summary:        Fast GF(256) Cauchy MDS Block Erasure Codec in C++
License:        GPL-3.0-or-later
URL:            https://github.com/f4exb/cm256cc
Source0:        cm256cc-1.1.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Fast GF(256) Cauchy MDS Block Erasure Codec in C++

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
