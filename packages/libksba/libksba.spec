# SPDX-License-Identifier: Apache-2.0
Name:           libksba
Version:        1.8.1
Release:        1%{?dist}
Summary:        CMS and X.509 certificate access library
License:        GPL-3.0-or-later AND LGPL-2.1-or-later AND (LGPL-3.0-or-later OR GPL-2.0-or-later)
URL:            https://gnupg.org/related_software/libksba/
Source0:        libksba-1.8.1.tar.bz2

BuildRequires:  gcc
BuildRequires:  gawk
BuildRequires:  libgcrypt-devel >= 1.2.0
BuildRequires:  libgpg-error-devel >= 1.28
BuildRequires:  make

%description
KSBA provides access to X.509 certificates and CMS objects used as building
blocks for S/MIME, GnuPG, and related security applications.

%package devel
Summary:        Development files for libksba
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libgpg-error-devel%{?_isa} >= 1.28
Requires:       pkgconfig

%description devel
Headers, configuration helpers, and unversioned library links for developing
applications with KSBA.

%prep
%autosetup -p1

%build
%configure \
  --disable-dependency-tracking \
  --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv3
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/libksba.so.8*

%files devel
%{_bindir}/ksba-config
%{_includedir}/ksba.h
%{_libdir}/libksba.so
%{_libdir}/pkgconfig/ksba.pc
%{_datadir}/aclocal/ksba.m4
%{_infodir}/ksba.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.0-1
- Initial openEuler RISC-V package with the complete upstream test suite.
