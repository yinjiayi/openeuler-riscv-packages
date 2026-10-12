# SPDX-License-Identifier: Apache-2.0
Name:           libjpeg-turbo
Version:        3.2.0
Release:        1%{?dist}
Summary:        SIMD-accelerated JPEG codec libraries and tools
License:        Zlib AND BSD-3-Clause AND MIT AND IJG
URL:            https://libjpeg-turbo.org/
Source0:        libjpeg-turbo-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  zlib-devel

%description
libjpeg-turbo is a JPEG image codec that uses SIMD instructions to accelerate
baseline compression and decompression. This package contains the libjpeg and
TurboJPEG shared libraries.

%package utils
Summary:        Utilities for manipulating JPEG images
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Command-line JPEG compression, decompression, transformation, comment, and
benchmark utilities.

%package devel
Summary:        Development files for libjpeg-turbo
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config and CMake metadata, and unversioned linker names for the
libjpeg and TurboJPEG APIs.

%package help
Summary:        Documentation for libjpeg-turbo
BuildArch:      noarch

%description help
Manual pages, API examples, and upstream release documentation.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DENABLE_SHARED=ON \
  -DENABLE_STATIC=OFF \
  -DFLOATTEST=fp-contract \
  -DWITH_SIMD=ON \
  -DWITH_TESTS=ON \
  -DWITH_TOOLS=ON \
  -DWITH_TURBOJPEG=ON
%cmake_build

%install
%cmake_install
rm -rf %{buildroot}%{_docdir}/%{name}

%check
%ctest --parallel 1

%files
%license LICENSE.md
%{_libdir}/libjpeg.so.62*
%{_libdir}/libturbojpeg.so.0*

%files utils
%license LICENSE.md
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/tjbench
%{_bindir}/wrjpgcom

%files devel
%license LICENSE.md
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_includedir}/turbojpeg.h
%{_libdir}/libjpeg.so
%{_libdir}/libturbojpeg.so
%{_libdir}/pkgconfig/libjpeg.pc
%{_libdir}/pkgconfig/libturbojpeg.pc
%{_libdir}/cmake/libjpeg-turbo/

%files help
%license LICENSE.md
%doc README.ijg README.md doc/libjpeg.txt doc/structure.txt doc/usage.txt doc/wizard.txt
%doc src/example.c src/tjcomp.c src/tjdecomp.c src/tjtran.c
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.0-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
