# SPDX-License-Identifier: Apache-2.0
Name:           libXvMC
Version:        1.0.15
Release:        1%{?dist}
Summary:        X Video Motion Compensation client libraries
License:        MIT AND HPND-sell-variant
URL:            https://gitlab.freedesktop.org/xorg/lib/libXvMC
Source0:        libXvMC-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXv-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXvMC provides the X Video Motion Compensation client library and its
wrapper library for X11 applications.

%package devel
Summary:        Development files for libXvMC
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       libXv-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, pkg-config metadata and linker names for the X Video Motion
Compensation client and wrapper libraries.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXvMC.la
rm -f %{buildroot}%{_libdir}/libXvMCW.la

%check
# Upstream registers no test programs; preserve its Automake check target.
%make_build check

%files
%license COPYING
%doc README.md
%{_docdir}/libXvMC/XvMC_API.txt
%{_libdir}/libXvMC.so.1*
%{_libdir}/libXvMCW.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/XvMClib.h
%{_includedir}/X11/extensions/vldXvMC.h
%{_libdir}/libXvMC.so
%{_libdir}/libXvMCW.so
%{_libdir}/pkgconfig/xvmc.pc
%{_libdir}/pkgconfig/xvmc-wrapper.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.15-1
- Package the official X.Org 1.0.15 release for openEuler RISC-V.
