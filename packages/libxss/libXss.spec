# SPDX-License-Identifier: Apache-2.0
Name:           libXss
Version:        1.2.5
Release:        1%{?dist}
Summary:        X Screen Saver extension client library
License:        X11
URL:            https://gitlab.freedesktop.org/xorg/lib/libxscrnsaver
Source0:        libXScrnSaver-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXss implements the client side of the X Screen Saver extension to the
X11 protocol.

%package devel
Summary:        Development files for libXss
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public header, pkg-config metadata, linker name, and manual pages for X
Screen Saver client applications.

%prep
%autosetup -n libXScrnSaver-%{version} -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libXss.la

%check
# Upstream registers no test programs; preserve its Automake check target.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXss.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/scrnsaver.h
%{_libdir}/libXss.so
%{_libdir}/pkgconfig/xscrnsaver.pc
%{_mandir}/man3/XScreenSaver*.3*
%{_mandir}/man3/Xss.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.5-1
- Package the official X.Org 1.2.5 release for openEuler RISC-V.
