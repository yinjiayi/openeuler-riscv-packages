# SPDX-License-Identifier: Apache-2.0
Name:           libconfig
Version:        1.8.2
Release:        1%{?dist}
Summary:        C and C++ library for structured configuration files
License:        LGPL-2.1-or-later AND GPL-3.0-or-later WITH Bison-exception-2.2
URL:            https://hyperrealm.github.io/libconfig/
Source0:        libconfig-%{version}.tar.gz

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  texinfo

%description
libconfig provides C and C++ APIs for reading, manipulating, and writing a
compact, type-aware structured configuration format.

%package devel
Summary:        Development files for libconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, unversioned library links, pkg-config data, CMake package metadata,
and documentation for software built against libconfig.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules \
    --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libconfig*.la
rm -f %{buildroot}%{_infodir}/dir

%check
%make_build check

%files
%license COPYING.LIB
%doc AUTHORS ChangeLog README
%{_libdir}/libconfig.so.15*
%{_libdir}/libconfig++.so.15*

%files devel
%license COPYING.LIB
%{_includedir}/libconfig.h
%{_includedir}/libconfig.h++
%{_libdir}/libconfig.so
%{_libdir}/libconfig++.so
%{_libdir}/pkgconfig/libconfig.pc
%{_libdir}/pkgconfig/libconfig++.pc
%{_libdir}/cmake/libconfig/
%{_libdir}/cmake/libconfig++/
%{_infodir}/libconfig.info*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8.2-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
