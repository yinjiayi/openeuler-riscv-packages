# SPDX-License-Identifier: Apache-2.0
Name:           hiredis
Version:        1.4.1
Release:        1%{?dist}
Summary:        Minimal C client library for Redis
License:        BSD-3-Clause
URL:            https://github.com/redis/hiredis
Source0:        hiredis-1.4.1.tar.gz
Patch0:         0001-tests-use-riscv-qemu-safe-timeout.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libevent-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  redis

%description
hiredis is a minimal C client for Redis providing synchronous, asynchronous,
SSL, and protocol-parser APIs.

%package devel
Summary:        Development files for hiredis
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and unversioned library links for
developing applications with hiredis and hiredis_ssl.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_SHARED_LIBS=ON \
  -DDISABLE_TESTS=OFF \
  -DENABLE_ASYNC_TESTS=ON \
  -DENABLE_NUGET=OFF \
  -DENABLE_SSL=ON \
  -DENABLE_SSL_TESTS=ON
%cmake_build

%install
%cmake_install

%check
export REDIS_SERVER=redis-server
export TEST_SSL=1
%ctest

%files
%license COPYING
%doc CHANGELOG.md README.md
%{_libdir}/libhiredis.so.1*
%{_libdir}/libhiredis_ssl.so.1*

%files devel
%license COPYING
%{_includedir}/hiredis/
%{_libdir}/libhiredis.so
%{_libdir}/libhiredis_ssl.so
%{_libdir}/pkgconfig/hiredis.pc
%{_libdir}/pkgconfig/hiredis_ssl.pc
%{_libdir}/cmake/hiredis/
%{_libdir}/cmake/hiredis_ssl/

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Keep the SSL reconnect timeout test enabled with a RISC-V QEMU-safe margin.
- Initial openEuler RISC-V package with offline Redis, SSL, and async tests.
