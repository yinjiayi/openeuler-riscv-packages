# SPDX-License-Identifier: Apache-2.0
Name:           uriparser
Version:        1.0.2
Release:        1%{?dist}
Summary:        Strictly RFC 3986 compliant URI parsing library
License:        BSD-3-Clause
URL:            https://uriparser.github.io/
Source0:        uriparser-%{version}.tar.bz2

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Uriparser is a fast, cross-platform URI parsing library written in C and
strictly compliant with RFC 3986.

%package devel
Summary:        Development files for uriparser
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, CMake metadata, and pkg-config
metadata for developing applications with uriparser.

%prep
%autosetup

%build
%cmake_conf \
  -DURIPARSER_BUILD_DOCS=OFF \
  -DURIPARSER_BUILD_TESTS=ON \
  -DURIPARSER_BUILD_TOOLS=ON \
  -DURIPARSER_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure --parallel 1

%files
%license COPYING.BSD-3-Clause
%doc AUTHORS ChangeLog README.md THANKS
%{_bindir}/uriparse
%{_libdir}/liburiparser.so.1*

%files devel
%license COPYING.BSD-3-Clause
%{_includedir}/uriparser/
%{_libdir}/cmake/uriparser-%{version}/
%{_libdir}/liburiparser.so
%{_libdir}/pkgconfig/liburiparser.pc

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.2-1
- Initial openEuler RISC-V package from Fedora 44 and cross-distribution evidence.
