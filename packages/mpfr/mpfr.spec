# SPDX-License-Identifier: Apache-2.0
Name:           mpfr
Version:        4.2.2
Release:        1%{?dist}
Summary:        Multiple-precision floating-point library with correct rounding
License:        LGPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://www.mpfr.org
Source0:        mpfr-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  make

%description
MPFR is a portable multiple-precision floating-point library based on GMP. It
provides well-defined semantics and correct rounding for supported operations.

%package devel
Summary:        Development files for MPFR
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}

%description devel
Headers, pkg-config metadata, the reference manual, and the unversioned shared
library link for developing applications with MPFR.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-shared \
  --enable-thread-safe
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
rm -f %{buildroot}%{_pkgdocdir}/COPYING
rm -f %{buildroot}%{_pkgdocdir}/COPYING.LESSER
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING COPYING.LESSER
%doc AUTHORS BUGS ChangeLog FAQ.html NEWS README TODO examples
%{_libdir}/libmpfr.so.6*

%files devel
%license COPYING COPYING.LESSER
%{_includedir}/mpfr.h
%{_includedir}/mpf2mpfr.h
%{_libdir}/libmpfr.so
%{_libdir}/pkgconfig/mpfr.pc
%{_infodir}/mpfr.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.2.2-1
- Initial openEuler RISC-V package based on Fedora 44 and corroborating release evidence.
