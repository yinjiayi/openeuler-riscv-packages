# SPDX-License-Identifier: Apache-2.0
Name:           libmd
Version:        1.2.0
Release:        1%{?dist}
Summary:        Message-digest functions from BSD systems
License:        BSD-3-Clause AND BSD-2-Clause AND ISC AND LicenseRef-Beerware AND LicenseRef-Public-Domain
URL:            https://hadrons.org/software/libmd
Source0:        libmd-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make

%description
libmd provides BSD-originated message-digest APIs, including MD2, MD4, MD5,
RIPEMD-160, SHA-1, SHA-2, and SHA-3 families.

%package devel
Summary:        Development files for libmd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, API manual pages, and the unversioned shared
library link for developing applications with libmd.

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
%license COPYING
%doc ChangeLog README
%{_libdir}/libmd.so.0*

%files devel
%license COPYING
%{_includedir}/*.h
%{_libdir}/libmd.so
%{_libdir}/pkgconfig/libmd.pc
%{_mandir}/man3/*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package using the latest non-regressing stable release.
