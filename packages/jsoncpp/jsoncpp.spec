# SPDX-License-Identifier: Apache-2.0
Name:           jsoncpp
Version:        1.9.8
Release:        1%{?dist}
Summary:        C++ library for interacting with JSON
License:        MIT
URL:            https://github.com/open-source-parsers/jsoncpp
Source0:        jsoncpp-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3

%description
JsonCpp is a C++ library for parsing, writing, and manipulating JSON values.

%package devel
Summary:        Development files for JsonCpp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and the unversioned library link for
developing applications with JsonCpp.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_OBJECT_LIBS=OFF \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DJSONCPP_WITH_POST_BUILD_UNITTEST=ON \
  -DJSONCPP_WITH_TESTS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/libjsoncpp.so.27*

%files devel
%license LICENSE
%{_includedir}/json/
%{_libdir}/libjsoncpp.so
%{_libdir}/pkgconfig/jsoncpp.pc
%{_libdir}/cmake/jsoncpp/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.9.8-1
- Initial openEuler RISC-V package.
