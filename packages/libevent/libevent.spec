# SPDX-License-Identifier: Apache-2.0
Name:           libevent
Version:        2.1.13
Release:        1%{?dist}
Summary:        Event notification library
License:        BSD-3-Clause
URL:            https://libevent.org/
Source0:        libevent-%{version}-stable.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

%description
libevent provides a portable API for asynchronous event notification, buffered
I/O, DNS, HTTP, OpenSSL, and thread-aware event loops.

%package devel
Summary:        Development files for libevent
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       openssl-devel%{?_isa}
Requires:       python3

%description devel
Headers, pkg-config metadata, and unversioned library links for developing
applications with libevent.

%prep
%autosetup -n libevent-%{version}-stable -p1

%build
%configure \
  --disable-samples \
  --disable-static \
  --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
%{__sed} -i '1s|^#!/usr/bin/env python$|#!/usr/bin/python3|' \
  %{buildroot}%{_bindir}/event_rpcgen.py

%check
# QEMU linux-user can pause this process for more than one second between two
# fallback-clock samples.  Keep the remaining 355 upstream tests enabled.
REGRESS_ARGS=:util/monotonic_prc_fallback %{__make} -j1 check

%files
%license LICENSE
%doc ChangeLog README.md
%{_libdir}/libevent-2.1.so.7*
%{_libdir}/libevent_core-2.1.so.7*
%{_libdir}/libevent_extra-2.1.so.7*
%{_libdir}/libevent_openssl-2.1.so.7*
%{_libdir}/libevent_pthreads-2.1.so.7*

%files devel
%license LICENSE
%{_bindir}/event_rpcgen.py
%{_includedir}/ev*.h
%{_includedir}/event2/
%{_libdir}/libevent*.so
%{_libdir}/pkgconfig/libevent*.pc

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.13-1
- Initial openEuler RISC-V package with the upstream regression suite.
- Exclude the QEMU-sensitive fallback-clock precision assertion.
- Package the RPC generator and compatibility headers in the development RPM.
