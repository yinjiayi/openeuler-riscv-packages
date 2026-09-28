# SPDX-License-Identifier: Apache-2.0
Name:           libwbxml
Version:        0.11.10
Release:        1%{?dist}
Summary:        Library and tools for Wireless Binary XML
License:        LGPL-2.1-or-later
URL:            https://github.com/libwbxml/libwbxml
Source0:        libwbxml-%{version}.tar.gz

BuildRequires:  check-devel
BuildRequires:  bash
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(English)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  pkgconf-pkg-config

%description
libwbxml converts Wireless Binary XML (WBXML) documents to and from XML.
The package includes the shared library and both command-line converters.

%package devel
Summary:        Development files for libwbxml
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       expat-devel
Requires:       pkgconf-pkg-config

%description devel
Public headers, linker name, pkg-config metadata, and CMake package files
for applications using libwbxml.

%prep
%autosetup -n libwbxml-libwbxml-%{version} -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DENABLE_INSTALL_DOC=OFF \
  -DENABLE_UNIT_TEST=ON \
  -DLIB_SUFFIX=64 \
  -DLIBWBXML_LIBRARIES_DIR=%{_libdir} \
  -DLIBDATA_INSTALL_DIR=%{_libdir} \
  -DCMAKE_INSTALL_LIBDIR=%{_lib}
%cmake_build

%install
%cmake_install

%check
# Check-devel enables the upstream API suite. Retain the complete CTest
# registration, including XML round-trips and malformed-input regressions.
%ctest --parallel 4 --no-tests=error

%files
%license COPYING GNU-LGPL
%doc BUGS ChangeLog README References THANKS TODO
%{_bindir}/wbxml2xml
%{_bindir}/xml2wbxml
%{_libdir}/libwbxml2.so.1*

%files devel
%license COPYING GNU-LGPL
%{_includedir}/libwbxml-1.1/
%{_libdir}/libwbxml2.so
%{_libdir}/pkgconfig/libwbxml2.pc
%{_libdir}/cmake/libwbxml2/

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11.10-1
- Package the official release with the complete registered CTest suite.
