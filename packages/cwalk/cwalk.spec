# SPDX-License-Identifier: Apache-2.0
Name:           cwalk
Version:        1.2.9
Release:        1%{?dist}
Summary:        Cross-platform path manipulation library for C
License:        MIT
URL:            https://likle.github.io/cwalk
Source0:        cwalk-%{version}.tar.gz
Patch0:         0001-cmake-version-shared-library.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
cwalk is a small C library for joining, normalizing, comparing, and traversing
paths using Unix or Windows path semantics.

%package devel
Summary:        Development files for cwalk
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Header, linker name, CMake metadata, and pkg-config metadata for cwalk.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DENABLE_TESTS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libcwalk.so.1*

%files devel
%{_includedir}/cwalk.h
%{_libdir}/libcwalk.so
%{_libdir}/cmake/cwalk/
%{_libdir}/pkgconfig/cwalk.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.9-1
- Initial package from the official 1.2.9 tag archive.
- Version the shared library and preserve the complete upstream CTest suite.
