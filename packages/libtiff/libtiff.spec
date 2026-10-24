# SPDX-License-Identifier: Apache-2.0
Name:           libtiff
Version:        4.7.2
Release:        1%{?dist}
Summary:        Library for reading and writing TIFF images
License:        libtiff
URL:            https://libtiff.gitlab.io/libtiff/
Source0:        tiff-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  jbigkit-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libwebp-devel
BuildRequires:  make
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  zstd-devel

%description
LibTIFF provides a shared library for reading and writing Tagged Image File
Format images, including common lossless and lossy compression formats.

%package devel
Summary:        Development files for LibTIFF
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
C and C++ headers, linker names, CMake files, and pkg-config metadata for
applications using LibTIFF.

%package tools
Summary:        TIFF image conversion and inspection utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Upstream command-line tools for creating, converting, and inspecting TIFF
images.

%prep
%autosetup -n tiff-%{version} -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -Dtiff-static=OFF \
  -Dtiff-tools=ON \
  -Dtiff-tests=ON \
  -Dtiff-contrib=ON \
  -Dtiff-docs=ON \
  -Djpeg-prefer-standard=ON \
  -Djpeg=ON \
  -Dsphinx=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE.md
%{_libdir}/libtiff.so.*
%{_libdir}/libtiffxx.so.*
%{_docdir}/tiff/manual/html/

%files devel
%license LICENSE.md
%{_includedir}/tiff*.h
%{_includedir}/tiff*.hxx
%{_libdir}/libtiff.so
%{_libdir}/libtiffxx.so
%{_libdir}/cmake/tiff/
%{_libdir}/pkgconfig/libtiff-4.pc

%files tools
%license LICENSE.md
%{_bindir}/*

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.7.2-1
- Package the official LibTIFF 4.7.2 release for openEuler RISC-V.
