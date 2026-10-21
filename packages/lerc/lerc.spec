# SPDX-License-Identifier: Apache-2.0

Name:           lerc
Version:        4.2.0
Release:        1%{?dist}
Summary:        Limited Error Raster Compression library
License:        Apache-2.0
URL:            https://github.com/Esri/lerc
Source0:        lerc-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
Lerc is an open-source image and raster format supporting rapid lossless and
controlled-error compression for integer and floating-point data.

%package devel
Summary:        Development files for Lerc
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, linker name, and pkg-config metadata for developing with Lerc.

%prep
%autosetup -p1

%build
%cmake_conf -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
%{__cxx} %{optflags} -std=c++17 \
  -Isrc/LercLib/include src/LercTest/main.cpp \
  -L%{_vpath_builddir} -lLerc %{build_ldflags} \
  -o %{_vpath_builddir}/LercTest
LD_LIBRARY_PATH="$PWD/%{_vpath_builddir}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  LERCTEST_NONINTERACTIVE=1 %{_vpath_builddir}/LercTest

%files
%license LICENSE NOTICE
%doc CHANGELOG.md README.md
%{_libdir}/libLerc.so.4*

%files devel
%{_includedir}/Lerc_c_api.h
%{_includedir}/Lerc_types.h
%{_libdir}/libLerc.so
%{_libdir}/pkgconfig/Lerc.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.0-1
- Initial openEuler RISC-V package with the complete maintained LercTest gate.
