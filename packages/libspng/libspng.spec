# SPDX-License-Identifier: Apache-2.0
Name:           libspng
Version:        0.7.4
Release:        1%{?dist}
Summary:        Simple and secure PNG decoding and encoding library
License:        BSD-2-Clause AND libpng-2.0
URL:            https://libspng.org
Source0:        libspng-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libpng-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  zlib-devel

%description
libspng is a C library for decoding and encoding Portable Network Graphics
images. It provides a compact API, validates all integer arithmetic, and is
designed for continuous fuzz testing.

%package devel
Summary:        Development files for libspng
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Header, pkg-config metadata, and the unversioned linker name for developing
applications with libspng.

%prep
%autosetup -p1

%build
%meson \
  -Ddev_build=true \
  -Dbuild_examples=true \
  -Dbenchmarks=false \
  -Doss_fuzz=false \
  -Duse_miniz=false
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE tests/images/PngSuite.LICENSE
%doc README.md
%{_libdir}/libspng.so.0*

%files devel
%license LICENSE
%{_includedir}/spng.h
%{_libdir}/libspng.so
%{_libdir}/pkgconfig/spng.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.4-1
- Package the official stable 0.7.4 release for RVA23.
- Preserve the complete upstream Meson correctness and malformed-input suite.
