# SPDX-License-Identifier: Apache-2.0
Name:           cminpack
Version:        1.3.14
Release:        1%{?dist}
%global upstream_commit 48c2b6ecd180ad134c626365e3092ba5dd5463a7
Summary:        C and C++ implementation of the MINPACK optimization library
License:        LicenseRef-Minpack
URL:            http://devernay.free.fr/hacks/cminpack/
Source0:        cminpack-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  python3

%description
CMinpack is a C and C++ rewrite of the MINPACK nonlinear equation and
least-squares solvers, with single, double, and extended precision variants.

%package devel
Summary:        Development files for CMinpack
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, CMake and pkg-config metadata, and unversioned linker names for all
three CMinpack precision variants.

%prep
%autosetup -n cminpack-%{upstream_commit} -p1

%build
%cmake_conf \
  -DBUILD_EXAMPLES=ON \
  -DBUILD_EXAMPLES_FORTRAN=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DCMINPACK_CROSSCHECK=ON \
  -DCMINPACK_PRECISION=all \
  -DUSE_BLAS=OFF \
  -DUSE_LAPACK=OFF
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure --parallel 1

%files
%license CopyrightMINPACK.txt
%doc README.md
%{_libdir}/libcminpack.so.1*
%{_libdir}/libcminpacks.so.1*
%{_libdir}/libcminpackld.so.1*

%files devel
%license CopyrightMINPACK.txt
%{_includedir}/cminpack-1/
%{_libdir}/libcminpack.so
%{_libdir}/libcminpacks.so
%{_libdir}/libcminpackld.so
%{_libdir}/pkgconfig/cminpack.pc
%{_libdir}/pkgconfig/cminpacks.pc
%{_libdir}/pkgconfig/cminpackld.pc
%{_datadir}/cminpack/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.14-1
- Initial openEuler RISC-V package with all 44 upstream and reference tests.
