# SPDX-License-Identifier: Apache-2.0

Name:           cglm
Version:        0.9.6
Release:        1%{?dist}
Summary:        Optimized OpenGL mathematics library for C
License:        MIT
URL:            https://github.com/recp/cglm
Source0:        cglm-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
cglm provides optimized vector, matrix, quaternion, camera, and transformation
operations for C programs using array and struct APIs.

%package devel
Summary:        Development files for cglm
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, linker name, CMake metadata, and pkg-config metadata for cglm.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DCGLM_SHARED=ON \
  -DCGLM_STATIC=OFF \
  -DCGLM_USE_TEST=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc CREDITS README.md
%{_libdir}/libcglm.so.0*

%files devel
%{_includedir}/cglm/
%{_libdir}/libcglm.so
%{_libdir}/cmake/cglm/
%{_libdir}/pkgconfig/cglm.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.6-1
- Initial openEuler RISC-V package with the complete upstream CTest aggregate.
