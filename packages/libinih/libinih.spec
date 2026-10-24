# SPDX-License-Identifier: Apache-2.0
Name:           libinih
Version:        62
Release:        1%{?dist}
Summary:        Lightweight INI file parser for C and C++
License:        BSD-3-Clause
URL:            https://github.com/benhoyt/inih
Source0:        inih-r%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config

%description
inih is a small INI parser with C and C++ interfaces. This package includes
both the inih C library and the INIReader C++ library.

%package devel
Summary:        Development files for libinih
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for applications using inih or INIReader.

%prep
%autosetup -n inih-r%{version} -p1

%build
%meson -Ddistro_install=true -Dwith_INIReader=true -Dtests=true
%meson_build

%install
%meson_install

%check
# Retain all 15 C parser configurations and the C++ INIReader example test.
%meson_test

%files
%license LICENSE.txt
%doc README.md
%{_libdir}/libinih.so.0*
%{_libdir}/libINIReader.so.0*

%files devel
%license LICENSE.txt
%{_includedir}/ini.h
%{_includedir}/INIReader.h
%{_libdir}/libinih.so
%{_libdir}/libINIReader.so
%{_libdir}/pkgconfig/inih.pc
%{_libdir}/pkgconfig/INIReader.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 62-1
- Package the official SHA-256-pinned inih r62 release with all upstream tests.
