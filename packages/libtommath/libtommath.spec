# SPDX-License-Identifier: Apache-2.0
Name:           libtommath
Version:        1.3.0
Release:        1%{?dist}
Summary:        Portable multiple-precision integer library
License:        Unlicense
URL:            https://www.libtom.net/LibTomMath/
Source0:        ltm-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc

%description
LibTomMath is a portable C library implementing efficient multiple-precision
integer arithmetic for number-theoretic applications.

%package devel
Summary:        Development files for LibTomMath
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Header, pkg-config and CMake metadata, and the unversioned linker name for
LibTomMath.

%package help
Summary:        Documentation for LibTomMath
BuildArch:      noarch

%description help
The LibTomMath reference manual and upstream release documentation.

%prep
%autosetup -p1 -n libtommath-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON \
  -DENABLE_CCACHE=OFF
%cmake_build

%install
%cmake_install

%check
%ctest --parallel 1

%files
%license LICENSE
%{_libdir}/libtommath.so.1*

%files devel
%license LICENSE
%{_includedir}/tommath.h
%{_libdir}/libtommath.so
%{_libdir}/pkgconfig/libtommath.pc
%{_libdir}/cmake/libtommath/

%files help
%license LICENSE
%doc README.md changes.txt doc/bn.pdf

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
