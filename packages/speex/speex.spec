# SPDX-License-Identifier: Apache-2.0
Name: speex
Version: 1.2.1
Release: 2%{?dist}
Summary: Patent-free speech codec
License: BSD-3-Clause
URL: https://www.speex.org/
Source0: speex-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: libogg-devel
BuildRequires: make
%description
Speex is an open speech codec optimized for voice.
%package devel
Summary: Development files for Speex
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Headers and pkg-config metadata for Speex.
%prep
%autosetup -p1
%build
%configure --disable-static --with-ogg
%make_build
%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
%check
%make_build check
%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_docdir}/%{name}/manual.pdf
%{_bindir}/speexdec
%{_bindir}/speexenc
%{_libdir}/libspeex.so.1*
%{_mandir}/man1/speex*.1*
%files devel
%{_includedir}/speex/
%{_datadir}/aclocal/speex.m4
%{_libdir}/libspeex.so
%{_libdir}/pkgconfig/speex.pc
%changelog
* Tue Sep 01 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-2
- Own the installed manual and Autoconf macro in the RPM manifests.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial package.
