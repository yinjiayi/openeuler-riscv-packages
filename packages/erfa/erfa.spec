# SPDX-License-Identifier: Apache-2.0
Name:           erfa
Version:        2.0.1
Release:        1%{?dist}
Summary:        Essential Routines for Fundamental Astronomy
License:        BSD-3-Clause
URL:            https://github.com/liberfa/erfa
Source0:        erfa-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconf

%description
ERFA is a C library containing the Standards of Fundamental Astronomy
algorithms, with project-specific naming and release management.

%package devel
Summary:        Development files for ERFA
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications with ERFA.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc INFO README.rst RELEASE.rst
%{_libdir}/liberfa.so.1*

%files devel
%license LICENSE
%{_includedir}/erfa.h
%{_includedir}/erfadatextra.h
%{_includedir}/erfaextra.h
%{_includedir}/erfam.h
%{_libdir}/liberfa.so
%{_libdir}/pkgconfig/erfa.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package with both complete upstream test programs.
