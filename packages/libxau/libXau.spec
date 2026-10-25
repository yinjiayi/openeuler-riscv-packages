# SPDX-License-Identifier: Apache-2.0
Name:           libXau
Version:        1.0.12
Release:        1%{?dist}
Summary:        X Window System authorization data library
License:        MIT
URL:            https://www.x.org/
Source0:        libXau-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  xorg-x11-proto-devel

%description
libXau reads and writes X Window System authorization records.

%package devel
Summary:        Development files for libXau
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xorg-x11-proto-devel

%description devel
The public header, pkg-config metadata, manual pages, and unversioned link
needed to develop applications using libXau.

%prep
%autosetup -p1 -n libXau-%{version}

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXau.la

%check
%make_build check
./Autest -file auth-roundtrip-test
test -s auth-roundtrip-test
rm -f auth-roundtrip-test

%files
%license COPYING
%doc AUTHORS README ChangeLog
%{_libdir}/libXau.so.6*

%files devel
%license COPYING
%{_includedir}/X11/Xauth.h
%{_libdir}/libXau.so
%{_libdir}/pkgconfig/xau.pc
%{_mandir}/man3/Xau*.3*

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.12-1
- Initial package from the official, SHA-256-pinned X.Org release.
