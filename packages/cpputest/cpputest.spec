# SPDX-License-Identifier: Apache-2.0
Name:           cpputest
Version:        4.0
Release:        1%{?dist}
Summary:        Unit testing and mocking framework for C and C++
License:        BSD-3-Clause
URL:            https://github.com/cpputest/cpputest
Source0:        cpputest-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
CppUTest is a lightweight unit testing and mocking framework for C and C++.
This package includes the libraries, headers, CMake modules, and pkg-config
metadata needed to build and run CppUTest test programs.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DEXTENSIONS=ON \
  -DTESTS=ON \
  -DTESTS_DETAILED=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_includedir}/CppUTest/
%{_includedir}/CppUTestExt/
%{_libdir}/libCppUTest.so
%{_libdir}/libCppUTestExt.a
%{_libdir}/pkgconfig/cpputest.pc
%{_libdir}/CppUTest/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-1
- Initial openEuler RISC-V package with the complete 77-case upstream gate.
