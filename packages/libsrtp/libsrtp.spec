# SPDX-License-Identifier: Apache-2.0
Name:           libsrtp
Version:        2.8.0
Release:        1%{?dist}
Summary:        Secure Real-time Transport Protocol library
License:        BSD-3-Clause
URL:            https://github.com/cisco/libsrtp
Source0:        libsrtp-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libpcap-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  procps-ng
BuildRequires:  zlib-devel

%description
libsrtp implements the Secure Real-time Transport Protocol and its supporting
cryptographic transforms for media applications.

%package devel
Summary:        Development files for libsrtp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, static library, pkg-config metadata, and unversioned library link for
developing applications with libsrtp.

%prep
%autosetup -p1

%build
%configure --enable-openssl
%make_build
%make_build shared_library

%install
%make_install

%check
%make_build runtest

%files
%license LICENSE
%doc CHANGES README.md
%{_libdir}/libsrtp2.so.1

%files devel
%license LICENSE
%{_includedir}/srtp2/
%{_libdir}/libsrtp2.a
%{_libdir}/libsrtp2.so
%{_libdir}/pkgconfig/libsrtp2.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.8.0-1
- Initial openEuler RISC-V package.
