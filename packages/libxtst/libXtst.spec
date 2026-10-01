# SPDX-License-Identifier: Apache-2.0
Name:           libXtst
Version:        1.2.5
Release:        1%{?dist}
Summary:        X11 Testing and Recording extension client library
License:        HPND AND HPND-sell-variant AND MIT AND MIT-open-group AND X11
URL:            https://gitlab.freedesktop.org/xorg/lib/libXtst
Source0:        libXtst-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXtst implements the X11 Testing and Recording extension client APIs.

%package devel
Summary:        Development files for libXtst
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       libXi-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, pkg-config metadata, and shared-library linker name for
X11 Testing and Recording extension clients.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXtst.la

%check
# The upstream Autotools release registers no test programs.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXtst.so.6*

%files devel
%license COPYING
%{_includedir}/X11/extensions/XTest.h
%{_includedir}/X11/extensions/record.h
%{_libdir}/libXtst.so
%{_libdir}/pkgconfig/xtst.pc
%{_mandir}/man3/XTest*.3*
%{_docdir}/libXtst/*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.5-1
- Package the official X.Org 1.2.5 release for openEuler RISC-V.
