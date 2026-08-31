# SPDX-License-Identifier: Apache-2.0
Name:           libmspack
Version:        0.11alpha
Release:        1%{?dist}
Summary:        Library for Microsoft compression formats
License:        LGPL-2.1-only
URL:            https://www.cabextract.org.uk/libmspack/
Source0:        libmspack-0.11alpha.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
Library for decompressing Microsoft Cabinet, CHM, HLP, and related formats.

%package devel
Summary:        Development files for libmspack
Requires:       libmspack%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and shared-library links for libmspack.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-silent-rules
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libmspack.la

%check
%make_build check

%ldconfig_scriptlets

%files
%license COPYING.LIB
%doc README NEWS AUTHORS ChangeLog TODO
%{_libdir}/libmspack.so.0*

%files devel
%doc doc/szdd_kwaj_format.html
%{_includedir}/mspack.h
%{_libdir}/libmspack.so
%{_libdir}/pkgconfig/libmspack.pc

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.11alpha-1
- Package libmspack 0.11alpha with the complete upstream check suite.
