# SPDX-License-Identifier: Apache-2.0
Name:           tinyxml2
Version:        11.0.0
Release:        1%{?dist}
Summary:        Small C++ XML parser library
License:        Zlib
URL:            https://github.com/leethomason/tinyxml2
Source0:        tinyxml2-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
TinyXML-2 is a small, efficient C++ XML parser with a simple DOM-style API.

%package devel
Summary:        Development files for TinyXML-2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header, CMake metadata, pkg-config metadata, and the unversioned library link
for developing applications with TinyXML-2.

%prep
%autosetup -p1

%build
%cmake_conf \
  -Dtinyxml2_SHARED_LIBS=ON \
  -Dtinyxml2_BUILD_TESTING=ON \
  -Dtinyxml2_INSTALL_PKGCONFIG=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE.txt
%doc readme.md
%{_libdir}/libtinyxml2.so.11*

%files devel
%license LICENSE.txt
%{_includedir}/tinyxml2.h
%{_libdir}/libtinyxml2.so
%{_libdir}/pkgconfig/tinyxml2.pc
%{_libdir}/cmake/tinyxml2/

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 11.0.0-1
- Initial openEuler RISC-V package.
