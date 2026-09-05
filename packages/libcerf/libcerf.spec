# SPDX-License-Identifier: Apache-2.0
Name:           libcerf
Version:        3.6
Release:        1%{?dist}
Summary:        Complex error function library
License:        MIT
URL:            https://jugit.fz-juelich.de/mlz/libcerf
Source0:        libcerf-v3.6.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-podlators
BuildRequires:  pkgconf

%description
libcerf provides efficient C and C++ implementations of complex error
functions, including the Faddeeva, Dawson, and Voigt functions.

%package devel
Summary:        Development files for libcerf
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The C and C++ header, pkg-config and CMake metadata, manual pages, and the
unversioned shared library links for developing applications with libcerf.

%prep
%autosetup -n cerf-v%{version}-c5cef03b1d1da25990b433ee1daf7b3a5776df85 -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DCERF_C=ON \
  -DCERF_CPP=ON \
  -DLIB_MAN=ON \
  -DLIB_RUN=ON
%cmake_build

%install
%cmake_install
rm -rf %{buildroot}%{_docdir}/cerf

%check
# Run all 18 registered C and C++ numerical tests.
%ctest

%files
%license LICENSE
%doc CHANGELOG README.md
%{_libdir}/libcerf.so.3*
%{_libdir}/libcerfcpp.so.3*

%files devel
%license LICENSE
%{_includedir}/cerf.h
%{_libdir}/cmake/cerf/
%{_libdir}/libcerf.so
%{_libdir}/libcerfcpp.so
%{_libdir}/pkgconfig/libcerf.pc
%{_mandir}/man3/*.3*

%changelog
* Sat Sep 05 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.6-1
- Update to upstream 3.6 and retain the complete C and C++ test suite.

* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5-2
- Synchronize the archive root with the verified upstream v3.5 source.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3-1
- Initial openEuler RISC-V package with all 18 upstream C and C++ tests.
