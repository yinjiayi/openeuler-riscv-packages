# SPDX-License-Identifier: Apache-2.0
Name:           snappy
Version:        1.2.2
Release:        1%{?dist}
Summary:        Fast compression and decompression library
License:        BSD-3-Clause
URL:            https://github.com/google/snappy
Source0:        snappy-%{version}.tar.gz
Patch0:         0001-cmake-use-system-googletest.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  make

%description
Snappy is a compression and decompression library designed for very high
speeds and reasonable compression ratios.

%package devel
Summary:        Development files for Snappy
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, and the unversioned library link for developing
applications with Snappy.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DSNAPPY_BUILD_BENCHMARKS=OFF \
  -DSNAPPY_BUILD_TESTS=ON \
  -DSNAPPY_INSTALL=ON \
  -DSNAPPY_REQUIRE_AVX=OFF \
  -DSNAPPY_REQUIRE_AVX2=OFF
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license COPYING
%doc AUTHORS NEWS README.md
%{_libdir}/libsnappy.so.1*

%files devel
%license COPYING
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so
%{_libdir}/cmake/Snappy/

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.2-1
- Initial openEuler RISC-V package using system GoogleTest for upstream tests.
