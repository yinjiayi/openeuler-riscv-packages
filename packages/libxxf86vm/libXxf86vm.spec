# SPDX-License-Identifier: Apache-2.0
Name:           libXxf86vm
Version:        1.1.7
Release:        1%{?dist}
Summary:        XFree86 Video Mode extension client library
License:        X11 AND MIT
URL:            https://gitlab.freedesktop.org/xorg/lib/libxxf86vm
Source0:        libXxf86vm-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXxf86vm implements the client side of the XFree86 Video Mode extension
to the X11 protocol.

%package devel
Summary:        Development files for libXxf86vm
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public header, pkg-config metadata, linker name and manual pages for XFree86
Video Mode client applications.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXxf86vm.la

%check
# Upstream registers no test programs; preserve its Automake check target.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXxf86vm.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/xf86vmode.h
%{_libdir}/libXxf86vm.so
%{_libdir}/pkgconfig/xxf86vm.pc
%{_mandir}/man3/XF86*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.7-1
- Package the official X.Org 1.1.7 release for openEuler RISC-V.
