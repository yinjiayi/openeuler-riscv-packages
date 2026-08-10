# SPDX-License-Identifier: Apache-2.0
Name:           libuv
Version:        1.52.1
Release:        1%{?dist}
Summary:        Asynchronous I/O support library
License:        MIT
URL:            https://github.com/libuv/libuv
Source0:        libuv-1.52.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make


%description
libuv is a cross-platform asynchronous I/O library focused on event-driven
network and filesystem operations.

%package devel
Summary:        Development files for libuv
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, static library, pkg-config files, and CMake metadata for libuv.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_TESTING=ON \
  -DENABLE_CLANG_TIDY=OFF \
  -DLIBUV_BUILD_BENCH=OFF \
  -DLIBUV_BUILD_SHARED=ON \
  -DLIBUV_BUILD_TESTS=ON \
  -DQEMU=ON
%cmake_build

%install
%cmake_install

%check
# rpmbuild runs as root.  This is the upstream-supported opt-in that keeps the
# complete test suite enabled in that environment.
UV_RUN_AS_ROOT=1 %ctest

%files
%license LICENSE LICENSE-extra
%doc README.md
%{_libdir}/libuv.so.1*

%files devel
%license LICENSE LICENSE-extra
%{_includedir}/uv.h
%{_includedir}/uv/
%{_libdir}/libuv.so
%{_libdir}/libuv_a.a
%{_libdir}/cmake/libuv/
%{_libdir}/pkgconfig/libuv.pc
%{_libdir}/pkgconfig/libuv-static.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.52.1-1
- Initial openEuler RISC-V package.
