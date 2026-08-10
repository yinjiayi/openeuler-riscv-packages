# SPDX-License-Identifier: Apache-2.0
Name:           brotli
Version:        1.2.0
Release:        1%{?dist}
Summary:        Generic-purpose lossless compression library
License:        MIT
URL:            https://github.com/google/brotli
Source0:        brotli-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Brotli is a general-purpose lossless compression algorithm. This package
contains the command-line tool and shared encoder, decoder, and common
libraries.

%package devel
Summary:        Development files for Brotli
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, manual pages, and unversioned library links for
developing software with Brotli.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBROTLI_BUILD_TOOLS=ON \
  -DBROTLI_BUILD_FOR_PACKAGE=OFF \
  -DBROTLI_DISABLE_TESTS=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md
%{_bindir}/brotli
%{_libdir}/libbrotlicommon.so.*
%{_libdir}/libbrotlidec.so.*
%{_libdir}/libbrotlienc.so.*
%{_mandir}/man1/brotli.1*

%files devel
%license LICENSE
%{_includedir}/brotli/
%{_libdir}/libbrotlicommon.so
%{_libdir}/libbrotlidec.so
%{_libdir}/libbrotlienc.so
%{_libdir}/pkgconfig/libbrotlicommon.pc
%{_libdir}/pkgconfig/libbrotlidec.pc
%{_libdir}/pkgconfig/libbrotlienc.pc
%{_mandir}/man3/constants.h.3*
%{_mandir}/man3/decode.h.3*
%{_mandir}/man3/encode.h.3*
%{_mandir}/man3/types.h.3*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package.
