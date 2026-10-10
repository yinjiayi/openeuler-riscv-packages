# SPDX-License-Identifier: Apache-2.0
Name:           libXrandr
Version:        1.5.5
Release:        1%{?dist}
Summary:        X Resize, Rotate and Reflection extension client library
License:        HPND-sell-variant
URL:            https://gitlab.freedesktop.org/xorg/lib/libxrandr
Source0:        libXrandr-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrender-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXrandr implements the client side of the X Resize, Rotate and Reflection
extension to the X11 protocol.

%package devel
Summary:        Development files for libXrandr
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       libXrender-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public header, pkg-config metadata, linker name, and manual pages for RandR
client applications.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXrandr.la

%check
# Upstream registers no test programs; preserve its Automake check target.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXrandr.so.2*

%files devel
%license COPYING
%{_includedir}/X11/extensions/Xrandr.h
%{_libdir}/libXrandr.so
%{_libdir}/pkgconfig/xrandr.pc
%{_mandir}/man3/XRR*.3*
%{_mandir}/man3/Xrandr.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.5-1
- Package the official X.Org 1.5.5 release for openEuler RISC-V.
