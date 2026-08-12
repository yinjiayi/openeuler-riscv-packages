# SPDX-License-Identifier: Apache-2.0
Name:           CharLS
Version:        2.4.4
Release:        1%{?dist}
Summary:        JPEG-LS image codec library
License:        BSD-3-Clause
URL:            https://github.com/team-charls/charls
Source0:        charls-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf

%description
CharLS is a C and C++ implementation of the JPEG-LS lossless and near-lossless
image compression standard.

%package devel
Summary:        Development files for CharLS
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, CMake and pkg-config metadata, and the unversioned linker name for
developing applications with CharLS.

%prep
%autosetup -n charls-%{version} -p1

%build
%cmake \
  -DBUILD_SHARED_LIBS=ON \
  -DCHARLS_BUILD_FUZZ_TEST=OFF \
  -DCHARLS_BUILD_SAMPLES=ON \
  -DCHARLS_BUILD_TESTS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE.md
%doc CHANGELOG.md README.md SECURITY.md
%{_libdir}/libcharls.so.2*

%files devel
%license LICENSE.md
%{_includedir}/charls/
%{_libdir}/libcharls.so
%{_libdir}/pkgconfig/charls.pc
%{_libdir}/cmake/charls/

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.4-1
- Update CharLS while preserving libcharls.so.2 and running its complete portable test registration.
