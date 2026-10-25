# SPDX-License-Identifier: Apache-2.0
Name:           libxcvt
Version:        0.1.3
Release:        1%{?dist}
Summary:        VESA CVT modeline generator library and command-line tool
License:        MIT AND HPND-sell-variant
URL:            https://gitlab.freedesktop.org/xorg/lib/libxcvt
Source0:        libxcvt-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config

%description
libxcvt provides the VESA CVT modeline generator library and the standalone
cvt command-line tool.

%package devel
Summary:        Development files for libxcvt
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Public headers, pkg-config metadata, and shared-library linker name for
libxcvt clients.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
# The upstream 0.1.3 Meson project registers no test cases.
%meson_test

%files
%license COPYING
%doc README.md
%{_bindir}/cvt
%{_libdir}/libxcvt.so.0*
%{_mandir}/man1/cvt.1*

%files devel
%license COPYING
%{_includedir}/libxcvt/*.h
%{_libdir}/libxcvt.so
%{_libdir}/pkgconfig/libxcvt.pc

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.3-1
- Package the official X.Org 0.1.3 release for openEuler RISC-V.
