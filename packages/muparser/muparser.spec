# SPDX-License-Identifier: Apache-2.0
Name:           muparser
Version:        2.3.5
Release:        1%{?dist}
%global upstream_commit fbafd7f8774af2b53f4d2de07c57353fcfc09216
Summary:        Fast mathematical expression parser library
License:        BSD-2-Clause
URL:            https://beltoforion.de/en/muparser/
Source0:        muparser-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf

%description
muparser is a fast, extensible C++ mathematical expression parser with a C
interface, user-defined variables, functions, operators, and bulk evaluation.

%package devel
Summary:        Development files for muparser
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, CMake and pkg-config metadata, and the unversioned linker name for
developing applications with muparser.

%prep
%autosetup -n muparser-%{upstream_commit} -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DENABLE_OPENMP=ON \
  -DENABLE_SAMPLES=ON \
  -DENABLE_WIDE_CHAR=OFF
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure --parallel 1

%files
%license LICENSE
%doc CHANGELOG README.md
%{_libdir}/libmuparser.so.2*

%files devel
%license LICENSE
%{_includedir}/muParser*.h
%{_libdir}/libmuparser.so
%{_libdir}/pkgconfig/muparser.pc
%{_libdir}/cmake/muparser/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.5-1
- Initial openEuler RISC-V package with the complete upstream ParserTest suite.
