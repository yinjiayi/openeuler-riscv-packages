# SPDX-License-Identifier: Apache-2.0
Name:           libspiro
Version:        20240903
Release:        1%{?dist}
Summary:        Library for drawing smooth curves from spiro control points
License:        GPL-3.0-or-later
URL:            https://github.com/fontforge/libspiro
Source0:        libspiro-20240903.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make


%description
libspiro converts spiro control points into smooth Bezier curves.

%package devel
Summary:        Development files for libspiro
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and pkg-config metadata for developing applications with libspiro.

%prep
%autosetup -p1
autoreconf -fi

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
%doc README.md
%{_libdir}/libspiro.so.1*

%files devel
%license COPYING
%{_includedir}/bezctx.h
%{_includedir}/spiro.h
%{_includedir}/spiroentrypoints.h
%{_libdir}/libspiro.so
%{_libdir}/pkgconfig/libspiro.pc
%{_mandir}/man3/libspiro.3*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 20240903-1
- Initial openEuler RISC-V package.
