# SPDX-License-Identifier: Apache-2.0

Name:           gf2x
Version:        1.3.0
Release:        1%{?dist}
Summary:        Fast arithmetic over the binary polynomial field
License:        GPL-3.0-or-later AND LGPL-2.1-or-later
URL:            https://gitlab.inria.fr/gf2x/gf2x
Source0:        gf2x-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
gf2x provides portable and optimized routines for multiplication of
polynomials over GF(2), the binary finite field.

%package devel
Summary:        Development files for gf2x
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
Headers, linker name, and pkg-config metadata for developing with gf2x.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING COPYING.LIB
%doc AUTHORS BUGS ChangeLog NEWS README
%{_libdir}/libgf2x.so.3*

%files devel
%{_includedir}/gf2x.h
%{_includedir}/gf2x/
%{_libdir}/libgf2x.so
%{_libdir}/pkgconfig/gf2x.pc

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package with the complete upstream test suite.
