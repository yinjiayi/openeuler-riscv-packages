# SPDX-License-Identifier: Apache-2.0
Name:           libucl
Version:        0.9.4
Release:        1%{?dist}
Summary:        Universal configuration language parser library
License:        BSD-2-Clause
URL:            https://github.com/vstakhov/libucl
Source0:        libucl-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
libucl implements a configuration language with JSON compatibility, macros,
variables, includes, schema validation, and multiple output formats.

%package devel
Summary:        Development files for libucl
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, and the unversioned linker name for developing
applications with libucl.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DENABLE_UTILS=ON \
  -DENABLE_URL_INCLUDE=OFF \
  -DENABLE_URL_SIGN=OFF \
  -DENABLE_LUA=OFF \
  -DENABLE_LUAJIT=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc ChangeLog.md README.md
%{_bindir}/ucl_chargen
%{_bindir}/ucl_objdump
%{_bindir}/ucl_tool
%{_libdir}/libucl.so.0*

%files devel
%license COPYING
%{_includedir}/ucl.h
%{_includedir}/ucl++.h
%{_libdir}/libucl.so
%{_datadir}/ucl/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.4-1
- Initial openEuler RISC-V package with the complete upstream CMake suite.
