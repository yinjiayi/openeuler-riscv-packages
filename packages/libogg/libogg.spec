# SPDX-License-Identifier: Apache-2.0
Name:           libogg
Epoch:          2
Version:        1.3.6
Release:        1%{?dist}
Summary:        Ogg bitstream format library
License:        BSD-3-Clause
URL:            https://xiph.org/ogg/
Source0:        libogg-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make

%description
Libogg provides primitives for creating, parsing, and manipulating Ogg
bitstreams.

%package devel
Summary:        Development files for libogg
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       automake

%description devel
Headers, the unversioned library link, pkg-config metadata, and the Autoconf
macro for developing applications with libogg.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libogg.la
rm -rf %{buildroot}%{_docdir}/libogg

%check
%make_build check

%files
%license COPYING
%doc AUTHORS CHANGES README.md
%{_libdir}/libogg.so.0*

%files devel
%license COPYING
%dir %{_includedir}/ogg
%{_includedir}/ogg/config_types.h
%{_includedir}/ogg/ogg.h
%{_includedir}/ogg/os_types.h
%{_libdir}/libogg.so
%{_libdir}/pkgconfig/ogg.pc
%{_datadir}/aclocal/ogg.m4

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2:1.3.6-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
