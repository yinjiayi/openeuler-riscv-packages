# SPDX-License-Identifier: Apache-2.0
Name:           libdeflate
Version:        1.26
Release:        1%{?dist}
Summary:        Optimized DEFLATE compression and decompression library
License:        MIT
URL:            https://github.com/ebiggers/libdeflate
Source0:        libdeflate-1.26.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel

%description
libdeflate is a library for fast raw DEFLATE, zlib, and gzip compression and
decompression. The package also contains compatible gzip and gunzip tools.

%package devel
Summary:        Development files for libdeflate
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, CMake metadata, pkg-config metadata, and the unversioned library link
for developing applications with libdeflate.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DLIBDEFLATE_BUILD_STATIC_LIB=OFF \
  -DLIBDEFLATE_BUILD_SHARED_LIB=ON \
  -DLIBDEFLATE_BUILD_GZIP=ON \
  -DLIBDEFLATE_BUILD_TESTS=ON \
  -DLIBDEFLATE_USE_SHARED_LIB=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc NEWS.md README.md
%{_bindir}/libdeflate-gzip
%{_bindir}/libdeflate-gunzip
%{_libdir}/libdeflate.so.0*

%files devel
%license COPYING
%{_includedir}/libdeflate.h
%{_libdir}/libdeflate.so
%{_libdir}/pkgconfig/libdeflate.pc
%{_libdir}/cmake/libdeflate/

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.25-1
- Initial openEuler RISC-V package.
