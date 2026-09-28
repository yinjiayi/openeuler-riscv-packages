# SPDX-License-Identifier: Apache-2.0
Name:           libedlib
Version:        1.2.7
Release:        1%{?dist}
Summary:        Edit-distance sequence alignment library
License:        MIT
URL:            https://github.com/Martinsos/edlib
Source0:        libedlib-%{version}.tar.gz
Patch0:         0001-cmake-release-version.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Edlib provides fast pairwise sequence alignment using edit distance.

%package devel
Summary:        Development files for libedlib
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public header, linker name, pkg-config metadata and CMake package files.

%prep
%autosetup -n edlib-%{version} -p1

%build
%cmake -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=ON \
  -DEDLIB_ENABLE_INSTALL=ON -DEDLIB_BUILD_EXAMPLES=ON \
  -DEDLIB_BUILD_UTILITIES=ON
%cmake_build

%install
%cmake_install

%check
# Keep the upstream CTest registration intact: all randomized and specific
# correctness tests run under QEMU-user, not the unrelated benchmark data.
%ctest --parallel 1

%files
%license LICENSE
%doc README.md
%{_libdir}/libedlib.so.1*

%files devel
%license LICENSE
%{_includedir}/edlib.h
%{_libdir}/libedlib.so
%{_libdir}/pkgconfig/edlib-1.pc
%{_libdir}/cmake/edlib/

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.7-1
- Package the official edlib 1.2.7 release and full upstream tests.
