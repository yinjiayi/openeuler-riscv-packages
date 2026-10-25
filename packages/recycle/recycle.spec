# SPDX-License-Identifier: Apache-2.0
Name:           recycle
Version:        7.0.0
Release:        1%{?dist}
Summary:        Simple resource pool for recycling resources in C++
License:        BSD-3-Clause
URL:            https://github.com/steinwurf/recycle
Source0:        recycle-7.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Simple resource pool for recycling resources in C++

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
%license LICENSE.rst
%doc README.rst

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
