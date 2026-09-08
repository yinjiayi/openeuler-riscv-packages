# SPDX-License-Identifier: Apache-2.0
Name:           libcue
Version:        2.3.0
Release:        1%{?dist}
Summary:        CUE sheet parsing library
License:        GPL-2.0-only AND BSD-2-Clause
URL:            https://github.com/lipnitsk/libcue
Source0:        libcue-%{version}.tar.gz

BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libcue parses CUE sheets and exposes their disc, track, index, and CD-TEXT
metadata through a compact C API.

%package devel
Summary:        Development files for libcue
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Header, pkg-config metadata, and the unversioned linker name for developing
applications with libcue.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc ChangeLog README.md
%{_libdir}/libcue.so.2*

%files devel
%license LICENSE
%{_includedir}/libcue.h
%{_includedir}/libcue/
%{_libdir}/libcue.so
%{_libdir}/pkgconfig/libcue.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Package the official stable libcue 2.3.0 release for RVA23.
- Preserve all six bundled CTest parser regressions.
