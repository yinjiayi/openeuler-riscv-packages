# SPDX-License-Identifier: Apache-2.0

Name:           liblo
Version:        0.36
Release:        1%{?dist}
Summary:        Lightweight Open Sound Control implementation
License:        LGPL-2.1-or-later
URL:            https://liblo.sourceforge.net/
Source0:        liblo-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
liblo is a lightweight implementation of the Open Sound Control protocol. It
supports UDP, TCP, UNIX-domain sockets, bundles, timetags, patterns, and C and
C++ client and server APIs.

%package tools
Summary:        Command-line Open Sound Control tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Command-line utilities for sending, receiving, and relaying Open Sound Control
messages with liblo.

%package devel
Summary:        Development files for liblo
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, the C++ wrapper, the unversioned shared-library link, and pkg-config
metadata for developing applications with liblo.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-doc
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/liblo.la

%check
%{__make} V=1 test

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/liblo.so.7*

%files tools
%license COPYING
%{_bindir}/oscdump
%{_bindir}/oscsend
%{_bindir}/oscsendfile

%files devel
%license COPYING
%{_includedir}/lo/
%{_libdir}/liblo.so
%{_libdir}/pkgconfig/liblo.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.36-1
- Initial openEuler RISC-V package with all four registered upstream tests.
