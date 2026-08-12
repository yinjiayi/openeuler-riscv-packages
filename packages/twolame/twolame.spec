# SPDX-License-Identifier: Apache-2.0
Name: twolame
Version: 0.4.0
Release: 1%{?dist}
Summary: MPEG Audio Layer 2 encoding library
License: LGPL-2.1-or-later
URL: https://www.twolame.org/
Source0: twolame-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: libsndfile-devel
BuildRequires: make
%description
TwoLAME is an MPEG Audio Layer 2 encoder derived from tooLAME.
%package devel
Summary: Development files for TwoLAME
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Headers and pkg-config metadata for TwoLAME.
%prep
%autosetup -p1
%build
%configure --disable-static
%make_build
%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
%check
%make_build check
%files
%license COPYING
%doc AUTHORS ChangeLog README
%{_bindir}/twolame
%{_libdir}/libtwolame.so.0*
%{_mandir}/man1/twolame.1*
%files devel
%{_includedir}/twolame.h
%{_libdir}/libtwolame.so
%{_libdir}/pkgconfig/twolame.pc
%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial package.
