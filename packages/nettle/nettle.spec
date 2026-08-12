# SPDX-License-Identifier: Apache-2.0
Name:           nettle
Version:        4.0
Release:        1%{?dist}
Summary:        Low-level cryptographic library
License:        LGPL-3.0-or-later OR GPL-2.0-or-later
URL:            https://www.lysator.liu.se/~nisse/nettle/
Source0:        nettle-%{version}.tar.gz

BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  m4
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
Nettle is a low-level cryptographic library designed to fit into a wide range
of applications. Hogweed provides its public-key algorithms using GMP.

%package devel
Summary:        Development files for Nettle and Hogweed
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gmp-devel

%description devel
Headers, linker names, and pkg-config metadata for Nettle and Hogweed.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-shared
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING.LESSERv3 COPYINGv2 COPYINGv3
%doc AUTHORS NEWS README
%{_bindir}/*
%{_libdir}/libhogweed.so.*
%{_libdir}/libnettle.so.*
%{_infodir}/nettle.info*
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/nettle/
%{_libdir}/libhogweed.so
%{_libdir}/libnettle.so
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0-1
- Initial openEuler RISC-V package with the complete upstream test suite.
