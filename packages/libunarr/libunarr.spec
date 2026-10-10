# SPDX-License-Identifier: Apache-2.0
Name:           libunarr
Version:        1.1.1
Release:        2%{?dist}
Summary:        A lightweight decompression library with support for rar, tar and zip archives.
License:        LGPL-3.0-or-later
URL:            https://github.com/selmf/unarr
Source0:        libunarr-1.1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libcmocka-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
A lightweight decompression library with support for rar, tar and zip archives.

%package devel
Summary:        Development files for libunarr
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Header, pkg-config metadata, CMake target metadata, and the unversioned linker
name for developing applications with libunarr.

%prep
%autosetup -p1 -n unarr-%{version}

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_INTEGRATION_TESTS=ON \
  -DBUILD_UNIT_TESTS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc README.md
%doc AUTHORS
%{_libdir}/libunarr.so.1*

%files devel
%license COPYING
%{_includedir}/unarr.h
%{_libdir}/libunarr.so
%{_libdir}/pkgconfig/libunarr.pc
%{_libdir}/cmake/unarr/

%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-2
- Match the official source archive root and run the complete upstream test set.
- Split runtime and development files and verify the installed API in smoke.

* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
