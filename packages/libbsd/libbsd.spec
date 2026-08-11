# SPDX-License-Identifier: Apache-2.0
Name:           libbsd
Version:        0.12.2
Release:        1%{?dist}
Summary:        Utility functions from BSD systems
License:        BSD-3-Clause AND BSD-2-Clause AND BSD-4-Clause-UC AND ISC AND LicenseRef-Beerware AND LicenseRef-Public-Domain
URL:            https://libbsd.freedesktop.org
Source0:        libbsd-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  libmd-devel
BuildRequires:  make

%description
libbsd provides commonly used BSD interfaces for software running on systems
whose native C library does not expose them.

%package devel
Summary:        Development files for libbsd
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libmd-devel%{?_isa}

%description devel
BSD compatibility headers, manual pages, pkg-config metadata, and the
unversioned shared-library link for developing applications with libbsd.

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
%doc ChangeLog README TODO
%{_libdir}/libbsd.so.0*

%files devel
%license COPYING
%{_includedir}/bsd/
%{_libdir}/libbsd.so
%{_libdir}/pkgconfig/libbsd.pc
%{_libdir}/pkgconfig/libbsd-ctor.pc
%{_libdir}/pkgconfig/libbsd-overlay.pc
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12.2-1
- Initial openEuler RISC-V package based on cross-distribution release evidence.
