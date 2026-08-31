# SPDX-License-Identifier: Apache-2.0
Name:           libcbor
Version:        0.14.0
Release:        1%{?dist}
Summary:        CBOR parsing and serialization library for C
License:        MIT
URL:            https://libcbor.org
Source0:        libcbor-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libcmocka-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libcbor is a compact C library for parsing and generating Concise Binary
Object Representation data. It implements RFC 8949 and RFC 8742 with no
runtime dependency beyond the C library.

%package devel
Summary:        Development files for libcbor
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, pkg-config metadata, CMake metadata, and the unversioned linker name
for developing applications with libcbor.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DWITH_TESTS=ON \
  -DWITH_EXAMPLES=OFF \
  -DSANITIZE=OFF
%cmake_build

%install
%cmake_install

%check
%ctest
%{_vpath_builddir}/test/cpp_linkage_test

%files
%license LICENSE.md
%doc CHANGELOG.md README.md
%{_libdir}/libcbor.so.0*

%files devel
%license LICENSE.md
%{_includedir}/cbor.h
%{_includedir}/cbor/
%{_libdir}/libcbor.so
%{_libdir}/pkgconfig/libcbor.pc
%{_libdir}/cmake/libcbor/

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14.0-1
- Package the official stable 0.14.0 release for RVA23.
- Preserve every registered CMocka test and the C++ linkage probe.
