# SPDX-License-Identifier: Apache-2.0
Name:           libmseed
Version:        3.5.4
Release:        1%{?dist}
%global upstream_commit d6e6ad306de5b7bdde072e5a5e3d58ddcc11abd8
Summary:        miniSEED seismic record library
License:        Apache-2.0
URL:            https://earthscope.github.io/libmseed/
Source0:        libmseed-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libcurl-devel
BuildRequires:  pkgconf

%description
libmseed reads and writes miniSEED seismological data records, including
format version 2 and 3. URL access is enabled through libcurl.

%package devel
Summary:        Development files for libmseed
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libcurl-devel%{?_isa}
Requires:       pkgconf

%description devel
Public C header, static library, unversioned shared-library link, CMake
configuration, and pkg-config metadata for developing with libmseed.

%prep
%autosetup -n libmseed-%{upstream_commit} -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_STATIC_LIBS=ON \
  -DBUILD_EXAMPLES=ON \
  -DBUILD_TESTS=ON \
  -DLIBMSEED_URL=ON
%cmake_build

%install
%cmake_install

%check
# Keep all registered upstream tests and their bundled reference records.
%ctest -- -j1

%files
%license LICENSE
%{_docdir}/libmseed/
%{_libdir}/libmseed.so.3*

%files devel
%license LICENSE
%{_includedir}/libmseed.h
%{_libdir}/libmseed.so
%{_libdir}/libmseed.a
%{_libdir}/pkgconfig/mseed.pc
%{_libdir}/cmake/libmseed/

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.5.4-1
- Initial package from the official SHA-256-pinned EarthScope release.
