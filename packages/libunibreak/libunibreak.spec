# SPDX-License-Identifier: Apache-2.0
Name:           libunibreak
Version:        7.0
Release:        1%{?dist}
Summary:        Unicode line and word breaking library
License:        Zlib
URL:            https://github.com/adah1972/libunibreak
Source0:        libunibreak-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
libunibreak implements Unicode line, word, and grapheme breaking algorithms
using the Unicode data bundled in the official release archive.

%package devel
Summary:        Development files for libunibreak
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
applications with libunibreak.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libunibreak.la

%check
%make_build check

%files
%license LICENCE
%doc AUTHORS NEWS README.md
%{_libdir}/libunibreak.so.7*

%files devel
%license LICENCE
%{_includedir}/eastasianwidthdef.h
%{_includedir}/graphemebreak.h
%{_includedir}/linebreak.h
%{_includedir}/linebreakdef.h
%{_includedir}/unibreakbase.h
%{_includedir}/unibreakdef.h
%{_includedir}/wordbreak.h
%{_libdir}/libunibreak.so
%{_libdir}/pkgconfig/libunibreak.pc

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 7.0-1
- Initial openEuler RISC-V package.
