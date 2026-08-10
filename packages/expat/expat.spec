# SPDX-License-Identifier: Apache-2.0
Name:           expat
Version:        2.8.2
Release:        1%{?dist}
Summary:        Stream-oriented XML parser library
License:        MIT
URL:            https://libexpat.github.io/
Source0:        expat-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  docbook-utils
BuildRequires:  gcc
BuildRequires:  make

%description
Expat is a stream-oriented XML parser library written in C. This package also
provides the xmlwf command-line well-formedness checker.

%package devel
Summary:        Development files for Expat
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and the unversioned library link for
developing applications with Expat.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DEXPAT_BUILD_DOCS=ON \
  -DEXPAT_BUILD_EXAMPLES=ON \
  -DEXPAT_BUILD_PKGCONFIG=ON \
  -DEXPAT_BUILD_TESTS=ON \
  -DEXPAT_BUILD_TOOLS=ON \
  -DEXPAT_ENABLE_INSTALL=ON \
  -DEXPAT_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc AUTHORS Changes README.md
%{_bindir}/xmlwf
%{_libdir}/libexpat.so.1*
%{_mandir}/man1/xmlwf.1*

%files devel
%license COPYING
%{_includedir}/expat*.h
%{_libdir}/libexpat.so
%{_libdir}/pkgconfig/expat.pc
%{_libdir}/cmake/expat-%{version}/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8.2-1
- Initial openEuler RISC-V package with upstream CTest coverage.
