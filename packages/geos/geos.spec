# SPDX-License-Identifier: Apache-2.0
Name:           geos
Version:        3.14.1
Release:        1%{?dist}
Summary:        Geometry Engine Open Source
License:        LGPL-2.1-only
URL:            https://libgeos.org/
Source0:        geos-%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
GEOS is a C++ geometry engine implementing the OpenGIS Simple Features
geometry model and operations. It also provides a stable C API for
applications and language bindings.

%package devel
Summary:        Development files for GEOS
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
C and C++ headers, unversioned shared-library links, CMake exports,
pkg-config metadata, and the geos-config helper for developing with GEOS.

%prep
%autosetup

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DBUILD_BENCHMARKS=OFF
%cmake_build

%install
%cmake_install

%check
CTEST_PARALLEL_LEVEL=1 %ctest --timeout 300 --output-on-failure

%files
%license COPYING
%doc AUTHORS NEWS.md README.md
%{_bindir}/geosop
%{_libdir}/libgeos.so.3*
%{_libdir}/libgeos_c.so.1*

%files devel
%license COPYING
%{_bindir}/geos-config
%{_includedir}/geos/
%{_includedir}/geos.h
%{_includedir}/geos_c.h
%{_libdir}/libgeos.so
%{_libdir}/libgeos_c.so
%{_libdir}/cmake/GEOS/
%{_libdir}/pkgconfig/geos.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.14.1-1
- Initial openEuler RISC-V package with the complete upstream CTest suite.
