# SPDX-License-Identifier: Apache-2.0
Name:           libp11
Version:        0.4.21
Release:        1%{?dist}
Summary:        PKCS#11 wrapper library and OpenSSL integration modules
License:        LGPL-2.1-or-later
URL:            https://github.com/OpenSC/libp11
Source0:        libp11-%{version}.tar.gz

BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  opensc
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  p11-kit-devel
BuildRequires:  pkgconf
BuildRequires:  softhsm

%description
libp11 provides a high-level PKCS#11 API for OpenSSL applications, together
with an OpenSSL 3 provider and a legacy PKCS#11 engine.

%package devel
Summary:        Development files for libp11
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, an unversioned linker name, and pkg-config metadata for applications
that use the libp11 PKCS#11 wrapper API.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --disable-api-doc \
  --with-enginesdir=%{_libdir}/engines-3 \
  --with-modulesdir=%{_libdir}/ossl-modules
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}%{_docdir}/%{name}

%check
# Exercise the complete upstream suite with the software PKCS#11 token.
make check

%files
%license COPYING
%doc NEWS README.md INSTALL.md
%{_libdir}/libp11.so.3*
%{_libdir}/engines-3/pkcs11.so
%{_libdir}/engines-3/libpkcs11.so
%{_libdir}/ossl-modules/pkcs11prov.so
%{_libdir}/ossl-modules/libpkcs11.so

%files devel
%license COPYING
%{_includedir}/libp11.h
%{_includedir}/p11_err.h
%{_includedir}/p11_ver.h
%{_libdir}/libp11.so
%{_libdir}/pkgconfig/libp11.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.21-1
- Initial package from the official 0.4.21 release with full SoftHSM tests.
