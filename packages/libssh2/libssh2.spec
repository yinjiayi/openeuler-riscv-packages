# SPDX-License-Identifier: Apache-2.0
Name:           libssh2
Version:        1.11.1
Release:        1%{?dist}
Summary:        Client-side C library implementing the SSH2 protocol
License:        BSD-3-Clause
URL:            https://libssh2.org
Source0:        libssh2-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  openssh-clients
BuildRequires:  openssh-server

%description
libssh2 is a client-side C library implementing the SSH2 protocol. It
provides shared-library, pkg-config, CMake, and manual-page interfaces for
applications that need SSH transport support.

%package devel
Summary:        Development files for libssh2
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned linker name, pkg-config and CMake metadata, and
manual pages for developing applications with libssh2.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DBUILD_STATIC_LIBS=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_TESTING=ON \
  -DCRYPTO_BACKEND=OpenSSL \
  -DENABLE_ZLIB_COMPRESSION=ON \
  -DRUN_DOCKER_TESTS=OFF \
  -DRUN_SSHD_TESTS=ON
%cmake_build

%install
%cmake_install
rm -f %{buildroot}%{_libdir}/libssh2.a
rm -rf %{buildroot}%{_docdir}/libssh2

%check
%ctest --output-on-failure --force-new-ctest-process -- -j1

%files
%license COPYING
%doc README.md NEWS RELEASE-NOTES
%{_libdir}/libssh2.so.1*

%files devel
%license COPYING
%{_includedir}/libssh2.h
%{_includedir}/libssh2_publickey.h
%{_includedir}/libssh2_sftp.h
%{_libdir}/libssh2.so
%{_libdir}/pkgconfig/libssh2.pc
%{_libdir}/cmake/libssh2/
%{_mandir}/man3/libssh2_*.3*

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.1-1
- Initial openEuler RISC-V package with the upstream CMake test suite.
