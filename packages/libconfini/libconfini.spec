# SPDX-License-Identifier: Apache-2.0
Name:           libconfini
Version:        1.16.4
Release:        1%{?dist}
Summary:        INI file parser library for C
License:        GPL-3.0-or-later
URL:            https://madmurphy.github.io/libconfini/
Source0:        libconfini-%{version}-with-configure.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
Libconfini parses INI files using callbacks and provides string and array
helpers for C applications.

%package devel
Summary:        Development files for libconfini
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public header, linker name, and pkg-config metadata for libconfini.

%prep
%autosetup -p1 -n libconfini-%{version}-with-configure

%build
%configure --disable-static || { status=$?; tail -n 120 config.log; exit "$status"; }
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build -j1 check

%files
%license COPYING
%doc README
%{_libdir}/libconfini.so.0*
%{_docdir}/libconfini/
%{_mandir}/man3/*

%files devel
%license COPYING
%{_includedir}/confini.h
%{_libdir}/libconfini.so
%{_libdir}/pkgconfig/libconfini.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16.4-1
- Package the official libconfini 1.16.4 release for openEuler RISC-V.
