# SPDX-License-Identifier: Apache-2.0
Name:           libXxf86dga
Version:        1.1.7
Release:        1%{?dist}
Summary:        X11 Direct Graphics Access extension client library
License:        X11
URL:            https://gitlab.freedesktop.org/xorg/lib/libxxf86dga
Source0:        libXxf86dga-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXxf86dga implements the client side of the XFree86 Direct Graphics Access
extension to the X11 protocol.

%package devel
Summary:        Development files for libXxf86dga
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, manual pages, pkg-config metadata, and shared-library linker
name for Direct Graphics Access clients.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
# The upstream 1.1.7 Meson project registers no test cases.
%meson_test

%files
%license COPYING
%doc README.md
%{_libdir}/libXxf86dga.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/Xxf86dga.h
%{_includedir}/X11/extensions/xf86dga1.h
%{_libdir}/libXxf86dga.so
%{_libdir}/pkgconfig/xxf86dga.pc
%{_mandir}/man3/*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.7-1
- Package the official X.Org 1.1.7 release for openEuler RISC-V.
