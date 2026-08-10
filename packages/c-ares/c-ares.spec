# SPDX-License-Identifier: Apache-2.0
Name:           c-ares
Version:        1.34.8
Release:        1%{?dist}
Summary:        Asynchronous DNS request library
License:        MIT
URL:            https://c-ares.org/
Source0:        c-ares-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
BuildRequires:  make

%description
c-ares is a C library for asynchronous DNS requests, including a resolver
library and diagnostic command-line tools.

%package devel
Summary:        Development files for c-ares
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, manual pages, pkg-config metadata, CMake metadata, and the
unversioned library link for developing applications with c-ares.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DCMAKE_NO_SYSTEM_FROM_IMPORTED=ON \
  -DCARES_BUILD_TESTS=ON \
  -DCARES_BUILD_TOOLS=ON \
  -DCARES_INSTALL=ON \
  -DCARES_SHARED=ON \
  -DCARES_STATIC=OFF \
  -DCARES_THREADS=ON
%cmake_build

%install
%cmake_install

%check
# Network is disabled during package builds. Keep every deterministic upstream
# unit/fuzz-corpus test while excluding only tests explicitly named Live*.
GTEST_FILTER='-*Live*' %ctest

%files
%license LICENSE.md
%doc AUTHORS README.md RELEASE-NOTES.md SECURITY.md
%{_bindir}/adig
%{_bindir}/ahost
%{_libdir}/libcares.so.2*
%{_mandir}/man1/adig.1*
%{_mandir}/man1/ahost.1*

%files devel
%license LICENSE.md
%{_includedir}/ares*.h
%{_libdir}/libcares.so
%{_libdir}/pkgconfig/libcares.pc
%{_libdir}/cmake/c-ares/
%{_mandir}/man3/ares*.3*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.34.8-1
- Initial openEuler RISC-V package with offline upstream tests.
