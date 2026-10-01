# SPDX-License-Identifier: Apache-2.0
Name:           libXfixes
Version:        6.0.2
Release:        1%{?dist}
Summary:        X Fixes extension client library
License:        HPND-sell-variant AND MIT
URL:            https://gitlab.freedesktop.org/xorg/lib/libxfixes
Source0:        libXfixes-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  xorg-x11-proto-devel

%description
libXfixes implements the client side of the X Fixes extension to the X11
protocol.

%package devel
Summary:        Development files for libXfixes
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, pkg-config metadata, and linker name for X Fixes clients.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
# The upstream 6.0.2 Meson project registers no test cases.
%meson_test

%files
%license COPYING
%doc README.md
%{_libdir}/libXfixes.so.3*

%files devel
%license COPYING
%{_includedir}/X11/extensions/Xfixes.h
%{_libdir}/libXfixes.so
%{_libdir}/pkgconfig/xfixes.pc
%{_mandir}/man3/Xfixes.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.2-1
- Package the official X.Org 6.0.2 release for openEuler RISC-V.
