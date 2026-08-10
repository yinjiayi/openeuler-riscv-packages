# SPDX-License-Identifier: Apache-2.0
Name:           json-c
Version:        0.19
Release:        1%{?dist}
Summary:        JSON implementation in C
License:        MIT
URL:            https://github.com/json-c/json-c
Source0:        json-c-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
json-c implements reference-counted JSON objects, parsing, serialization,
JSON Pointer, and JSON Patch for C applications.

%package devel
Summary:        Development files for json-c
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and the unversioned library link for
developing applications with json-c.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_APPS=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=OFF \
  -DBUILD_TESTING=ON \
  -DENABLE_THREADING=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_libdir}/libjson-c.so.5*

%files devel
%license COPYING
%{_includedir}/json-c/
%{_libdir}/libjson-c.so
%{_libdir}/pkgconfig/json-c.pc
%{_libdir}/cmake/json-c/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.19-1
- Initial openEuler RISC-V package.
