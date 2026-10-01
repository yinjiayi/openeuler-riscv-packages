# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}

Name:           cpp-httplib
Version:        0.54.1
Release:        2%{?dist}
Summary:        Header-only C++ HTTP and HTTPS library
License:        MIT
URL:            https://github.com/yhirose/cpp-httplib
Source0:        v0.54.1.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make

%description
cpp-httplib is a single-header C++11 HTTP client and server library. This
package intentionally installs the dependency-free header-only variant; TLS
and compression feature variants are not silently selected from the build
host.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DHTTPLIB_COMPILE=OFF \
  -DHTTPLIB_INSTALL=ON \
  -DHTTPLIB_TEST=OFF \
  -DHTTPLIB_USE_OPENSSL_IF_AVAILABLE=OFF \
  -DHTTPLIB_USE_WOLFSSL_IF_AVAILABLE=OFF \
  -DHTTPLIB_USE_MBEDTLS_IF_AVAILABLE=OFF \
  -DHTTPLIB_USE_ZLIB_IF_AVAILABLE=OFF \
  -DHTTPLIB_USE_BROTLI_IF_AVAILABLE=OFF \
  -DHTTPLIB_USE_ZSTD_IF_AVAILABLE=OFF
%cmake_build

%install
%cmake_install
rm -rf %{buildroot}%{_docdir}/httplib
rm -rf %{buildroot}%{_datadir}/licenses/httplib

%check
%{__cxx} %{optflags} -std=c++11 -pthread -I. \
  example/server_and_client.cc -o server-and-client-test
./server-and-client-test > server-and-client.log
grep -F 'Success' server-and-client.log
grep -F 'POST' server-and-client.log

%files
%license LICENSE
%doc README.md
%{_includedir}/httplib.h
%{_libdir}/cmake/httplib/

%changelog
* Wed Sep 02 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.54.1-2
- Synchronize the installed smoke assertion and package documentation with 0.54.1.

* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.52.0-1
- Initial openEuler RISC-V package.
