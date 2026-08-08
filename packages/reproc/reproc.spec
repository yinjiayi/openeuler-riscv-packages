# SPDX-License-Identifier: Apache-2.0
Name:           reproc
Version:        14.2.7
Release:        1%{?dist}
Summary:        Cross-platform C and C++ process execution library
License:        MIT
URL:            https://github.com/DaanDeMeyer/reproc
Source0:        reproc-14.2.7.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
reproc is a cross-platform library for starting, stopping, and communicating
with child processes from C and C++.

%package devel
Summary:        Development files for reproc
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, pkg-config files, and unversioned library links for
developing software with reproc and reproc++.

%prep
%autosetup -p1

%build
%cmake \
  -DBUILD_SHARED_LIBS=ON \
  -DREPROC++=ON \
  -DREPROC_TEST=ON \
  -DREPROC_EXAMPLES=OFF \
  -DREPROC_INSTALL=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_libdir}/libreproc.so.14*
%{_libdir}/libreproc++.so.14*

%files devel
%license LICENSE
%{_includedir}/reproc/
%{_includedir}/reproc++/
%{_libdir}/libreproc.so
%{_libdir}/libreproc++.so
%{_libdir}/pkgconfig/reproc.pc
%{_libdir}/pkgconfig/reproc++.pc
%{_libdir}/cmake/reproc/
%{_libdir}/cmake/reproc++/

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 14.2.7-1
- Initial openEuler RISC-V package.

