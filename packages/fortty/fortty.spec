# SPDX-License-Identifier: Apache-2.0
Name:           fortty
Version:        0.1.7
Release:        1%{?dist}
Summary:        GPU-accelerated terminal emulator written in Fortran
License:        MIT
URL:            https://github.com/FortranGoingOnForty/fortty
Source0:        fortty-0.1.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
GPU-accelerated terminal emulator written in Fortran

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.7-1
- Initial openEuler RISC-V package from the full package inventory.
