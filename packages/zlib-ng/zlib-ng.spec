# SPDX-License-Identifier: Apache-2.0
%undefine _cmake_shared_libs

Name:           zlib-ng
Version:        2.3.3
Release:        1%{?dist}
Summary:        Zlib replacement with next-generation optimizations
License:        Zlib
URL:            https://github.com/zlib-ng/zlib-ng
Source0:        zlib-ng-%{version}.tar.gz
Patch0:         0001-riscv-build-zbc-without-rvv.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Zlib-ng is a zlib replacement that provides a native API and optimized
implementations for modern processor architectures.

%package devel
Summary:        Development files for zlib-ng
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, CMake metadata, and pkg-config
metadata for developing applications with the native zlib-ng API.

%package static
Summary:        Static library for zlib-ng
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The static zlib-ng library, built together with the shared library so the
complete upstream GoogleTest suite remains enabled.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_TESTING=ON \
  -DINSTALL_UTILS=OFF \
  -DWITH_GTEST=ON \
  -DWITH_RVV=OFF \
  -DWITH_RISCV_ZBC=OFF \
  -UBUILD_SHARED_LIBS
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure --parallel 1

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libz-ng.so.2*

%files devel
%license LICENSE.md
%{_includedir}/zconf-ng.h
%{_includedir}/zlib-ng.h
%{_includedir}/zlib_name_mangling-ng.h
%{_libdir}/cmake/zlib-ng/
%{_libdir}/libz-ng.so
%{_libdir}/pkgconfig/zlib-ng.pc

%files static
%license LICENSE.md
%{_libdir}/libz-ng.a

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.3-1
- Initial openEuler RISC-V package from Fedora 44 and cross-distribution evidence.
