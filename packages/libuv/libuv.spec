# SPDX-License-Identifier: Apache-2.0
Name:           libuv
Version:        1.52.1
Release:        1%{?dist}
Summary:        Asynchronous I/O support library
License:        MIT AND CC-BY-4.0 AND ISC AND BSD-2-Clause
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
# CMake installs duplicate license copies into the buildroot.  RPM's %license
# directive below copies the reviewed source files into the canonical location.
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE
rm -f %{buildroot}%{_docdir}/%{name}/LICENSE-extra
rmdir %{buildroot}%{_docdir}/%{name}

%check
# rpmbuild runs as root.  This is the upstream-supported opt-in that keeps the
# complete shared/static test suite enabled in that environment.  Exporting is
# required because the RPM CTest helper changes directory before launching it.
export UV_RUN_AS_ROOT=1
export UV_TEST_TIMEOUT_MULTIPLIER=10
# openEuler's RPM macro supplies the build-wide -j value before explicit
# arguments.  Keep the shared and static test executables serialized so they
# cannot contend for the same ports and temporary paths.
%ctest --parallel 1

%files
%license LICENSE LICENSE-docs LICENSE-extra
%doc AUTHORS CONTRIBUTING.md ChangeLog MAINTAINERS.md README.md SUPPORTED_PLATFORMS.md
%{_libdir}/libuv.so.1*

%files devel
%license LICENSE LICENSE-docs LICENSE-extra
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
