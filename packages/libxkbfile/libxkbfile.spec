# SPDX-License-Identifier: Apache-2.0
Name:           libxkbfile
Version:        1.2.0
Release:        1%{?dist}
Summary:        XKB configuration file parsing library
License:        MIT
URL:            https://gitlab.freedesktop.org/xorg/lib/libxkbfile
Source0:        libxkbfile-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libX11-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  xorg-x11-proto-devel

%description
libxkbfile provides routines used by X servers and utilities to parse XKB
keyboard configuration files.

%package devel
Summary:        Development files for libxkbfile
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Headers, pkg-config metadata, and the linker name for applications using
libxkbfile.

%prep
%autosetup -n libxkbfile-42e5dedd7fd3c7c73f3870a8751893c03c1afc69 -p1

%build
%meson
%meson_build

%install
%meson_install

%check
# The upstream 1.2.0 Meson project registers no test cases.
%meson_test

%files
%license COPYING
%doc README.md
%{_libdir}/libxkbfile.so.1*

%files devel
%license COPYING
%{_includedir}/X11/extensions/XKBbells.h
%{_includedir}/X11/extensions/XKBconfig.h
%{_includedir}/X11/extensions/XKBfile.h
%{_includedir}/X11/extensions/XKBrules.h
%{_includedir}/X11/extensions/XKM.h
%{_includedir}/X11/extensions/XKMformat.h
%{_libdir}/libxkbfile.so
%{_libdir}/pkgconfig/xkbfile.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Package the official X.Org 1.2.0 release for openEuler RISC-V.
