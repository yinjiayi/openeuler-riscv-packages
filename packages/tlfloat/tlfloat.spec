# SPDX-License-Identifier: Apache-2.0
Name:           tlfloat
Version:        1.15.0
Release:        1%{?dist}
Summary:        C++ template library for floating point operations
License:        BSL-1.0
URL:            https://github.com/shibatch/tlfloat
Source0:        tlfloat-1.15.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ template library for floating point operations

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


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.15.0-1
- Initial openEuler RISC-V package from the full package inventory.
