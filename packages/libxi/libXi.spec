# SPDX-License-Identifier: Apache-2.0
Name:           libXi
Version:        1.8.3
Release:        1%{?dist}
Summary:        X11 Input extension client library
License:        HPND AND MIT AND MIT-open-group
URL:            https://gitlab.freedesktop.org/xorg/lib/libXi
Source0:        libXi-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXi implements the client side of the X Input extension to the X11
protocol.

%package devel
Summary:        Development files for libXi
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       libXfixes-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, manual pages, pkg-config metadata, and shared-library linker
name for X Input extension clients.

%prep
%autosetup -p1

%build
%configure --disable-docs --disable-specs
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Upstream 1.8.3 registers no Automake test programs or TESTS.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXi.so.6*

%files devel
%license COPYING
%{_includedir}/X11/extensions/XInput.h
%{_includedir}/X11/extensions/XInput2.h
%{_libdir}/libXi.so
%{_libdir}/pkgconfig/xi.pc
%{_mandir}/man3/*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.3-1
- Package the official X.Org 1.8.3 release for openEuler RISC-V.
