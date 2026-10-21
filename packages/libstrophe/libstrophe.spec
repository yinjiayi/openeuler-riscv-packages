# SPDX-License-Identifier: Apache-2.0
Name: libstrophe
Version: 0.14.0
Release: 1%{?dist}
Summary: Lightweight XMPP client library
License: MIT AND GPL-3.0-or-later
URL: https://strophe.im/libstrophe/
Source0: libstrophe-%{version}.tar.gz
BuildRequires: expat-devel
BuildRequires: gcc
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: zlib-devel
%description
libstrophe is a minimal XMPP client library written in C.
%package devel
Summary: Development files for libstrophe
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Headers and pkg-config metadata for libstrophe.
%prep
%autosetup -p1
%build
%configure --disable-static --with-tls=openssl
%make_build
%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
%check
%make_build check
%files
%license COPYING MIT-LICENSE.txt GPL-LICENSE.txt
%doc ChangeLog README
%{_libdir}/libstrophe.so.0*
%files devel
%{_includedir}/strophe.h
%{_libdir}/libstrophe.so
%{_libdir}/pkgconfig/libstrophe.pc
%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.14.0-1
- Initial package.
