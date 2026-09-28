# SPDX-License-Identifier: Apache-2.0
Name:           libXfont2
Version:        2.0.9
Release:        1%{?dist}
Summary:        X.Org server-side font handling library
License:        BSD-2-Clause AND BSD-4-Clause-UC AND HPND-sell-variant AND MIT-open-group AND SMLNJ AND X11
URL:            https://gitlab.freedesktop.org/xorg/lib/libXfont
Source0:        libXfont2-%{version}.tar.xz

BuildRequires:  freetype-devel
BuildRequires:  gcc
BuildRequires:  libfontenc-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-xtrans-devel
BuildRequires:  zlib-devel

%description
libXfont2 implements server-side font discovery and rendering for X.Org.

%package devel
Summary:        Development files for libXfont2
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       freetype-devel
Requires:       libfontenc-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel
Requires:       zlib-devel

%description devel
Public header, pkg-config metadata, and shared-library linker name for
X.Org font clients such as the X server.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXfont2.la

%check
# Python generates malformed PCF fixtures for five upstream security tests.
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog README.md
%{_libdir}/libXfont2.so.2*

%files devel
%license COPYING
%doc doc/fontlib.xml
%{_includedir}/X11/fonts/libxfont2.h
%{_libdir}/libXfont2.so
%{_libdir}/pkgconfig/xfont2.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.9-1
- Package the official X.Org 2.0.9 release for openEuler RISC-V.
