# SPDX-License-Identifier: Apache-2.0
Name:           npth
Version:        1.8
Release:        1%{?dist}
Summary:        GNU portable non-preemptive threads library
License:        LGPL-2.1-or-later
URL:            https://gnupg.org/software/npth/
Source0:        npth-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make

%description
nPth supplies a cooperative-threading API on top of the system POSIX threads
implementation for GnuPG and other event-driven applications.

%package devel
Summary:        Development files for nPth
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Headers, pkg-config metadata, and unversioned library links for developing
applications with nPth.

%prep
%autosetup -p1

%build
%configure \
  --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la

%check
%make_build check

%files
%license COPYING.LIB
%{_libdir}/libnpth.so.0*

%files devel
%doc AUTHORS ChangeLog NEWS README
%{_includedir}/npth.h
%{_libdir}/libnpth.so
%{_libdir}/pkgconfig/npth.pc
%{_datadir}/aclocal/npth.m4

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Initial openEuler RISC-V package with the complete upstream test suite.
