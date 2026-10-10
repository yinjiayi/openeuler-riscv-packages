# SPDX-License-Identifier: Apache-2.0
Name:           libXmu
Version:        1.3.1
Release:        1%{?dist}
Summary:        X11 miscellaneous utility libraries
License:        MIT-open-group AND SMLNJ AND X11 AND ISC
URL:            https://gitlab.freedesktop.org/xorg/lib/libxmu
Source0:        libXmu-%{version}.tar.xz
Patch0:         0001-reallocarray-test-avoid-qemu-ignored-rlimit.patch

BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXt-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXmu provides X11 miscellaneous utility routines, including the smaller
libXmuu interface that does not require Xt widgets.

%package devel
Summary:        Development files for libXmu and libXmuu
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libX11-devel
Requires:       libXext-devel
Requires:       libXt-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public headers, pkg-config metadata, and linker names for libXmu and libXmuu.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-docs --enable-unit-tests
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Run all 11 upstream GLib unit-test executables; do not disable their suite.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXmu.so.6*
%{_libdir}/libXmuu.so.1*

%files devel
%license COPYING
%{_includedir}/X11/Xmu/*.h
%{_libdir}/libXmu.so
%{_libdir}/libXmuu.so
%{_libdir}/pkgconfig/xmu.pc
%{_libdir}/pkgconfig/xmuu.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Package the official X.Org 1.3.1 release for openEuler RISC-V.
