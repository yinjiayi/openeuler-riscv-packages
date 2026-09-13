# SPDX-License-Identifier: Apache-2.0
Name: serd
Version: 0.32.10
Release: 1%{?dist}
Summary: Lightweight RDF syntax library
License: ISC
URL: https://drobilla.net/software/serd.html
Source0: serd-%{version}.tar.xz
BuildRequires: gcc
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: python3

%description
Serd is a lightweight C library for reading and writing RDF syntax.

%package devel
Summary: Development files for Serd
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, library link, and pkg-config metadata for Serd.

%prep
%autosetup -p1

%build
%meson -Dtests=enabled -Ddocs=disabled -Dman_html=disabled -Dlint=false
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc NEWS README.md
%{_bindir}/serdi
%{_libdir}/libserd-0.so.0*
%{_mandir}/man1/serdi.1*

%files devel
%{_includedir}/serd-0/
%{_libdir}/libserd-0.so
%{_libdir}/pkgconfig/serd-0.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.32.10-1
- Initial openEuler RISC-V package from frozen lineage and official source evidence.
