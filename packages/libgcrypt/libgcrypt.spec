# SPDX-License-Identifier: Apache-2.0
Name:           libgcrypt
Version:        1.12.3
Release:        1%{?dist}
Summary:        General-purpose cryptographic library
License:        LGPL-2.1-or-later AND GPL-2.0-or-later AND BSD-3-Clause
URL:            https://gnupg.org/software/libgcrypt/
Source0:        libgcrypt-1.12.3.tar.bz2

BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  libgpg-error-devel >= 1.56
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
Requires:       libgpg-error%{?_isa} >= 1.56

%description
Libgcrypt is a general-purpose cryptographic library based on the code used by
the GNU Privacy Guard project.

%package devel
Summary:        Development files for libgcrypt
Requires:       libgcrypt%{?_isa} = %{version}-%{release}
Requires:       libgpg-error-devel%{?_isa} >= 1.56
Requires:       pkgconf-pkg-config

%description devel
Headers, linker metadata, and development configuration for applications using
libgcrypt.

%prep
%autosetup -p1

%build
%configure --disable-static --enable-noexecstack --disable-jent-support \
  --disable-O-flag-munging
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}%{_sysconfdir}/gcrypt

%check
%make_build check

%ldconfig_scriptlets

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS THANKS
%dir %{_sysconfdir}/gcrypt
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%{_libdir}/libgcrypt.so.*

%files devel
%{_bindir}/libgcrypt-config
%{_includedir}/gcrypt.h
%{_libdir}/libgcrypt.so
%{_libdir}/pkgconfig/libgcrypt.pc
%{_datadir}/aclocal/libgcrypt.m4
%{_infodir}/gcrypt.info*
%{_mandir}/man1/*

%changelog
* Tue Sep 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.2-2
- Match the development manifest to the single public header installed by upstream 1.12.2.

* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.12.2-1
- Package libgcrypt with all upstream algorithms and the complete check suite.
