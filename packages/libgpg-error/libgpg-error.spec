# SPDX-License-Identifier: Apache-2.0
Name:           libgpg-error
Version:        1.61
Release:        1%{?dist}
Summary:        Common error code library for GnuPG components
License:        LGPL-2.1-or-later AND (BSD-3-Clause OR LGPL-2.1-or-later) AND FSFULLR AND GPL-2.0-or-later
URL:            https://www.gnupg.org/related_software/libgpg-error/
Source0:        libgpg-error-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  gawk
BuildRequires:  gettext
BuildRequires:  gettext-devel
BuildRequires:  make
BuildRequires:  texinfo

%description
Libgpg-error defines common error values and utility functions shared by
GnuPG, GPGME, libgcrypt, libassuan, and related security components.

%package devel
Summary:        Development files for libgpg-error
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Headers, configuration helpers, and unversioned library links for developing
applications that use libgpg-error and libgpgrt.

%prep
%autosetup -p1

%build
%configure \
  --disable-languages \
  --disable-rpath \
  --disable-static \
  --enable-install-gpg-error-config
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
%find_lang %{name}

%check
%make_build check

%files -f %{name}.lang
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_bindir}/gpg-error
%{_libdir}/libgpg-error.so.0*
%{_datadir}/libgpg-error/

%files devel
%{_bindir}/gpg-error-config
%{_bindir}/gpgrt-config
%{_bindir}/yat2m
%{_includedir}/gpg-error.h
%{_includedir}/gpgrt.h
%{_libdir}/libgpg-error.so
%{_libdir}/pkgconfig/gpg-error.pc
%{_datadir}/aclocal/gpg-error.m4
%{_datadir}/aclocal/gpgrt.m4
%{_infodir}/gpgrt.info*
%{_mandir}/man1/gpg-error-config.1*
%{_mandir}/man1/gpgrt-config.1*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.61-1
- Initial openEuler RISC-V package with the complete upstream test suite.
