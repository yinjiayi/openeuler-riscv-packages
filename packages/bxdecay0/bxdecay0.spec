# SPDX-License-Identifier: Apache-2.0
Name:           bxdecay0
Version:        1.1.2
Release:        1%{?dist}
Summary:        C++ port of the legacy Decay0 FORTRAN library
License:        GPL-3.0-or-later
URL:            https://github.com/BxCppDev/bxdecay0
Source0:        bxdecay0-1.1.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ port of the legacy Decay0 FORTRAN library

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
%doc README.rst

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
