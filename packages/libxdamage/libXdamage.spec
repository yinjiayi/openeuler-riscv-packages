# SPDX-License-Identifier: Apache-2.0
Name:           libXdamage
Version:        1.1.7
Release:        1%{?dist}
Summary:        X Damage extension client library
License:        HPND-sell-variant AND MIT
URL:            https://gitlab.freedesktop.org/xorg/lib/libXdamage
Source0:        libXdamage-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXfixes-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXdamage implements the client side of the X Damage extension to the X11
protocol.

%package devel
Summary:        Development files for libXdamage
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXfixes-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public header, pkg-config metadata, and shared-library linker name for
X Damage clients.

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
%{_libdir}/libXdamage.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/Xdamage.h
%{_libdir}/libXdamage.so
%{_libdir}/pkgconfig/xdamage.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.7-1
- Package the official X.Org 1.1.7 release for openEuler RISC-V.
