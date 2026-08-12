# SPDX-License-Identifier: Apache-2.0
Name:           librsync
Version:        2.3.4
Release:        1%{?dist}
Summary:        Remote delta-compression library and rdiff utility
License:        LGPL-2.1-or-later AND CC0-1.0
URL:            https://github.com/librsync/librsync
Source0:        librsync-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  popt-devel

%description
librsync implements the rsync remote-delta algorithm without requiring
communication between the two systems. The package also provides the rdiff
command-line utility.

%package devel
Summary:        Development files for librsync
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, API documentation, and the unversioned shared-library link for
developing applications with librsync.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_RDIFF=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DUSE_LIBB2=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc AUTHORS NEWS.md README.md THANKS
%{_bindir}/rdiff
%{_libdir}/librsync.so.2*
%{_mandir}/man1/rdiff.1*

%files devel
%license COPYING
%{_includedir}/librsync.h
%{_includedir}/librsync_export.h
%{_libdir}/librsync.so
%{_mandir}/man3/librsync.3*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.4-1
- Initial openEuler RISC-V package with shared ABI, rdiff, and all 15 tests.
