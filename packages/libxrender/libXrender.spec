# SPDX-License-Identifier: Apache-2.0
Name:           libXrender
Version:        0.9.12
Release:        1%{?dist}
Summary:        X Render extension client library
License:        HPND-sell-variant
URL:            https://gitlab.freedesktop.org/xorg/lib/libXrender
Source0:        libXrender-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXrender implements the client side of the X Render extension to the X11
protocol.

%package devel
Summary:        Development files for libXrender
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, pkg-config metadata, and linker name for X Render clients.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXrender.la

%check
# The upstream 0.9.12 Automake project registers no test programs.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXrender.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/Xrender.h
%{_libdir}/libXrender.so
%{_libdir}/pkgconfig/xrender.pc
%{_docdir}/libXrender/libXrender.txt

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.12-1
- Package the official X.Org 0.9.12 release for openEuler RISC-V.
