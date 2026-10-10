# SPDX-License-Identifier: Apache-2.0
Name:           libXext
Version:        1.3.7
Release:        1%{?dist}
Summary:        X11 extension client library
License:        MIT-open-group AND X11 AND HPND AND HPND-sell-variant AND SMLNJ AND MIT AND ISC AND HPND-doc AND HPND-doc-sell
URL:            https://gitlab.freedesktop.org/xorg/lib/libXext
Source0:        libXext-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXext provides the client-side implementation for common X11 protocol
extensions.

%package devel
Summary:        Development files for libXext
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, pkg-config metadata, man pages, and the shared-library linker
name for X11 extension clients.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-specs --without-xmlto --without-fop --without-xsltproc
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXext.la

%check
# The upstream 1.3.7 Automake project registers no test programs.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXext.so.6*

%files devel
%license COPYING
%{_includedir}/X11/extensions/*.h
%{_libdir}/libXext.so
%{_libdir}/pkgconfig/xext.pc
%{_mandir}/man3/*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.7-1
- Package the official X.Org 1.3.7 release for openEuler RISC-V.
