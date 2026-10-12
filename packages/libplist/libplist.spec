# SPDX-License-Identifier: Apache-2.0
Name:           libplist
Version:        2.7.0
Release:        1%{?dist}
Summary:        C and C++ libraries for Apple property list files
License:        LGPL-2.1-or-later AND MIT
URL:            https://libimobiledevice.org/
Source0:        libplist-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libplist reads and writes Apple property list files in binary, XML, JSON,
and OpenStep formats. This package includes the C and C++ shared libraries
and the plistutil conversion tool.

%package devel
Summary:        Development files for libplist
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public C and C++ headers, unversioned linker names, and pkg-config metadata
for applications that read or write property lists.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --without-cython \
  --with-tools \
  --with-tests
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libplist-2.0.la
rm -f %{buildroot}%{_libdir}/libplist++-2.0.la

%check
%make_build check

%files
%license COPYING.LESSER libcnary/COPYING src/jsmn.c src/jsmn.h src/time64.c
%doc AUTHORS NEWS README.md
%{_bindir}/plistutil
%{_libdir}/libplist-2.0.so.*
%{_libdir}/libplist++-2.0.so.*
%{_mandir}/man1/plistutil.1*

%files devel
%license COPYING.LESSER libcnary/COPYING src/jsmn.c src/jsmn.h src/time64.c
%{_includedir}/plist/
%{_libdir}/libplist-2.0.so
%{_libdir}/libplist++-2.0.so
%{_libdir}/pkgconfig/libplist-2.0.pc
%{_libdir}/pkgconfig/libplist++-2.0.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.7.0-1
- Initial openEuler RISC-V package with the complete upstream test suite.
