# SPDX-License-Identifier: Apache-2.0
Name:           moordyn
Version:        2.6.1
Release:        1%{?dist}
Summary:        MoorDyn is a lumped-mass model for simulating the dynamics of mooring systems connected to floating offshore structures
License:        BSD-3-Clause
URL:            https://github.com/FloatingArrayDesign/MoorDyn
Source0:        moordyn-2.6.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
MoorDyn is a lumped-mass model for simulating the dynamics of mooring systems connected to floating offshore structures

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.1-1
- Initial openEuler RISC-V package from the full package inventory.
