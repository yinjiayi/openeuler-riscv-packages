# SPDX-License-Identifier: Apache-2.0
Name:           libxlsxwriter
Version:        1.2.4
Release:        1%{?dist}
Summary:        C library for creating Excel XLSX files
License:        BSD-2-Clause AND BSD-3-Clause AND Zlib AND MPL-2.0 AND MIT AND LicenseRef-Public-Domain
URL:            https://libxlsxwriter.github.io
Source0:        libxlsxwriter-%{version}.tar.gz
Patch0:         0001-cmake-honor-gnu-installdirs.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3-pytest
BuildRequires:  zlib-devel

%description
libxlsxwriter is a C library for creating Excel 2007 and later XLSX files.
It supports worksheets, formatting, formulas, charts, images, tables, and
memory-optimized output without requiring Excel.

%package devel
Summary:        Development files for libxlsxwriter
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config
Requires:       zlib-devel%{?_isa}

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with libxlsxwriter.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTS=ON \
  -DBUILD_EXAMPLES=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license License.txt
%doc Changes.txt Readme.md
%{_libdir}/libxlsxwriter.so.11*

%files devel
%license License.txt
%{_includedir}/xlsxwriter.h
%{_includedir}/xlsxwriter/
%{_libdir}/libxlsxwriter.so
%{_libdir}/pkgconfig/xlsxwriter.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.4-1
- Package the official stable 1.2.4 release for RVA23.
- Run the complete bundled unit and functional test suites.
