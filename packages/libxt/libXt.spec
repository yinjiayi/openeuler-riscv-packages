# SPDX-License-Identifier: Apache-2.0
Name:           libXt
Version:        1.3.1
Release:        1%{?dist}
Summary:        X Toolkit Intrinsics library
License:        MIT AND HPND AND MIT-open-group AND X11
URL:            https://gitlab.freedesktop.org/xorg/lib/libxt
Source0:        libXt-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  xorg-x11-proto-devel

%description
libXt implements the X Toolkit Intrinsics API for X11 applications.

%package devel
Summary:        Development files for libXt
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libICE-devel
Requires:       libSM-devel
Requires:       libX11-devel
Requires:       pkgconf-pkg-config
Requires:       xorg-x11-proto-devel

%description devel
Public X Toolkit headers, manual pages, pkg-config metadata, and linker name.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-specs --enable-unit-tests
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Run all three upstream GLib unit-test executables without excluding cases.
%make_build check

%files
%license COPYING
%doc README.md
%{_libdir}/libXt.so.6*

%files devel
%license COPYING
%{_includedir}/X11/*.h
%{_libdir}/libXt.so
%{_libdir}/pkgconfig/xt.pc
%{_mandir}/man3/*.3*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.1-1
- Package the official X.Org 1.3.1 release for openEuler RISC-V.
