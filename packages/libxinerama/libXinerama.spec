# SPDX-License-Identifier: Apache-2.0
Name:           libXinerama
Version:        1.1.6
Release:        1%{?dist}
Summary:        X11 Xinerama extension client library
License:        MIT AND MIT-open-group AND X11
URL:            https://gitlab.freedesktop.org/xorg/lib/libxinerama
Source0:        libXinerama-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXinerama implements the client side of the Xinerama extension to the X11
protocol.

%package devel
Summary:        Development files for libXinerama
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, manual pages, pkg-config metadata, and shared-library linker
name for Xinerama extension clients.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
# The upstream 1.1.6 Meson project registers no test cases.
%meson_test

%files
%license COPYING
%doc README.md
%{_libdir}/libXinerama.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/Xinerama.h
%{_includedir}/X11/extensions/panoramiXext.h
%{_libdir}/libXinerama.so
%{_libdir}/pkgconfig/xinerama.pc
%{_mandir}/man3/Xinerama*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.6-1
- Package the official X.Org 1.1.6 release for openEuler RISC-V.
