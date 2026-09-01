# SPDX-License-Identifier: Apache-2.0
Name:           libdivsufsort
Version:        2.0.1
Release:        1%{?dist}
Summary:        Lightweight suffix-array construction library
License:        MIT
URL:            https://github.com/y-256/libdivsufsort
Source0:        libdivsufsort-%{version}.tar.gz
Patch0:         0001-cmake-version-and-libdir.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libdivsufsort is a C library implementing a fast, lightweight suffix-array
construction algorithm. It provides both 32-bit and 64-bit index APIs.

%package devel
Summary:        Development files for libdivsufsort
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, pkg-config metadata, and unversioned linker names for developing
applications with the 32-bit and 64-bit libdivsufsort APIs.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_EXAMPLES=ON \
  -DBUILD_DIVSUFSORT64=ON
%cmake_build

%install
%cmake_install

%check
printf 'banana\nmississippi\n' > %{_vpath_builddir}/suffix-input.txt
%{_vpath_builddir}/examples/suftest %{_vpath_builddir}/suffix-input.txt

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libdivsufsort.so.3*
%{_libdir}/libdivsufsort64.so.3*

%files devel
%license COPYING
%{_includedir}/divsufsort.h
%{_includedir}/divsufsort64.h
%{_libdir}/libdivsufsort.so
%{_libdir}/libdivsufsort64.so
%{_libdir}/pkgconfig/libdivsufsort.pc
%{_libdir}/pkgconfig/libdivsufsort64.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Package the official stable 2.0.1 tag for RVA23.
- Build both index-width APIs and run the upstream suffix-array verifier.
