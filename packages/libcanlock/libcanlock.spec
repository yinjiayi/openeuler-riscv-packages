# SPDX-License-Identifier: Apache-2.0
Name:           libcanlock
Version:        3.3.3
Release:        1%{?dist}
Summary:        RFC 8315 Netnews Cancel-Lock library and header parsers
License:        BSD-3-Clause AND ICU AND NLPL
URL:            https://micha.freeshell.org/libcanlock/
Source0:        libcanlock-%{version}.tar.bz2

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libcanlock creates and verifies RFC 8315 Netnews Cancel-Locks. It includes
the canlock command-line utility and the canlock-hp header-parser library
and utilities.

%package devel
Summary:        Development files for libcanlock and libcanlock-hp
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, linker names, pkg-config metadata, and API manuals for applications
using libcanlock and libcanlock-hp.

%prep
%autosetup -p1

%build
%configure --enable-shared --enable-static --enable-pc-files
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libcanlock.a
rm -f %{buildroot}%{_libdir}/libcanlock.la
rm -f %{buildroot}%{_libdir}/libcanlock-hp.a
rm -f %{buildroot}%{_libdir}/libcanlock-hp.la

%check
%make_build check

%files
%license COPYING hp/COPYING LICENSES/BSD-3-Clause.txt LICENSES/ICU.txt LICENSES/NLPL.txt
%doc README ChangeLog hp/README hp/ChangeLog_V0
%{_bindir}/canlock
%{_bindir}/canlock-mhp
%{_bindir}/canlock-hfp
%{_libdir}/libcanlock.so.3*
%{_libdir}/libcanlock-hp.so.3*
%{_mandir}/man1/canlock*.1*

%files devel
%license COPYING hp/COPYING LICENSES/BSD-3-Clause.txt LICENSES/ICU.txt LICENSES/NLPL.txt
%{_includedir}/libcanlock-3/
%{_libdir}/libcanlock.so
%{_libdir}/libcanlock-hp.so
%{_libdir}/pkgconfig/libcanlock-3.pc
%{_libdir}/pkgconfig/libcanlock-hp-3.pc
%{_mandir}/man3/cl_*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.3-1
- Package official 3.3.3 release with both upstream Automake test suites.
