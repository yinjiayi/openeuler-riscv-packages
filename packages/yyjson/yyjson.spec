# SPDX-License-Identifier: Apache-2.0
Name:           yyjson
Version:        0.12.0
Release:        2%{?dist}
Summary:        High-performance JSON library written in C
License:        MIT
URL:            https://github.com/ibireme/yyjson
Source0:        yyjson-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
yyjson is a high-performance JSON reader and writer implemented in C.

%package devel
Summary:        Development files for yyjson
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, and pkg-config metadata for yyjson.

%prep
%autosetup -p1

%build
%cmake -S . -B "%{__cmake_builddir}" \
  -DBUILD_SHARED_LIBS=ON \
  -DYYJSON_BUILD_TESTS=ON \
  -DYYJSON_INSTALL=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_libdir}/libyyjson.so.*

%files devel
%{_includedir}/yyjson.h
%{_libdir}/libyyjson.so
%{_libdir}/pkgconfig/yyjson.pc
%{_libdir}/cmake/yyjson/

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12.0-2
- Exercise the installed shared library without requiring a compiler at runtime.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12.0-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
