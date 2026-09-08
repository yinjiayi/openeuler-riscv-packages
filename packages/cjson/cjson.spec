# SPDX-License-Identifier: Apache-2.0
Name:           cjson
Version:        1.7.19
Release:        1%{?dist}
Summary:        Ultralightweight JSON parser in ANSI C
License:        MIT
URL:            https://github.com/DaveGamble/cJSON
Source0:        cjson-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
cJSON is a small ANSI C library for parsing, printing, and manipulating JSON.
This build also provides the companion cJSON utility library.

%package devel
Summary:        Development files for cJSON
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and unversioned library links for
developing software with cJSON and cJSON_Utils.

%prep
%autosetup -n cJSON-%{version} -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DENABLE_CJSON_TEST=ON \
  -DENABLE_CJSON_UTILS=ON \
  -DENABLE_CJSON_UNINSTALL=OFF
%cmake_build

%install
%cmake_install

%check
%ctest -- -j1

%files
%license LICENSE
%doc CHANGELOG.md CONTRIBUTORS.md README.md
%{_libdir}/libcjson.so.1*
%{_libdir}/libcjson_utils.so.1*

%files devel
%license LICENSE
%{_includedir}/cjson/
%{_libdir}/libcjson.so
%{_libdir}/libcjson_utils.so
%{_libdir}/pkgconfig/libcjson.pc
%{_libdir}/pkgconfig/libcjson_utils.pc
%{_libdir}/cmake/cJSON/

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7.19-1
- Initial openEuler RISC-V package using the latest non-regressing stable release.
