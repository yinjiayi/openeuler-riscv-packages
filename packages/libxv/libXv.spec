# SPDX-License-Identifier: Apache-2.0
Name:           libXv
Version:        1.0.13
Release:        1%{?dist}
Summary:        X Video extension client library
License:        SMLNJ AND HPND-sell-variant
URL:            https://gitlab.freedesktop.org/xorg/lib/libxv
Source0:        libXv-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXv implements the client side of the X Video extension to the X11
protocol.

%package devel
Summary:        Development files for libXv
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public header, pkg-config metadata, linker name, and manual pages for X
Video client applications.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXv.la

%check
# Upstream registers no test programs; preserve its Automake check target.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXv.so.1*

%files devel
%license COPYING
%doc man/xv-library-v2.2.txt
%{_includedir}/X11/extensions/Xvlib.h
%{_libdir}/libXv.so
%{_libdir}/pkgconfig/xv.pc
%{_mandir}/man3/Xv*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.13-1
- Package the official X.Org 1.0.13 release for openEuler RISC-V.
