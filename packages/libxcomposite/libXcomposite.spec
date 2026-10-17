# SPDX-License-Identifier: Apache-2.0
Name:           libXcomposite
Version:        0.4.7
Release:        1%{?dist}
Summary:        X11 Composite extension client library
License:        HPND-sell-variant AND MIT
URL:            https://gitlab.freedesktop.org/xorg/lib/libXcomposite
Source0:        libXcomposite-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXfixes-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXcomposite implements the client side of the Composite extension to the
X11 protocol.

%package devel
Summary:        Development files for libXcomposite
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXfixes-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public header, pkg-config metadata, and shared-library linker name for
Composite extension clients.

%prep
%autosetup -p1

%build
%meson -Ddocs=disabled
%meson_build

%install
%meson_install

%check
# The upstream 0.4.7 Meson project registers no test cases.
%meson_test

%files
%license COPYING
%doc README.md
%{_libdir}/libXcomposite.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/Xcomposite.h
%{_libdir}/libXcomposite.so
%{_libdir}/pkgconfig/xcomposite.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.7-1
- Package the official X.Org 0.4.7 release for openEuler RISC-V.
