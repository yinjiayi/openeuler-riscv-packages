# SPDX-License-Identifier: Apache-2.0
Name:           inih
Version:        62
Release:        1%{?dist}
Summary:        Simple INI file parser for C and C++
License:        BSD-3-Clause
URL:            https://github.com/benhoyt/inih
Source0:        inih-r%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  ninja-build

%description
inih is a small INI file parser written in C. This package also provides the
upstream C++ INIReader wrapper.

%package devel
Summary:        Development files for inih
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and unversioned library links for the C and C++
inih interfaces.

%prep
%autosetup -p1 -n inih-r%{version}

%build
%meson \
  -Ddistro_install=true \
  -Dwith_INIReader=true \
  -Dtests=true
%meson_build

%install
%meson_install

%check
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
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 62-1
- Initial openEuler RISC-V package.
