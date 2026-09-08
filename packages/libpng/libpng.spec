# SPDX-License-Identifier: Apache-2.0
Name:           libpng
Epoch:          2
Version:        1.6.58
Release:        1%{?dist}
Summary:        PNG reference library
License:        libpng-2.0
URL:            https://libpng.sourceforge.io/
Source0:        libpng-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel

%description
Libpng is the official reference library for reading, writing, and
manipulating Portable Network Graphics images.

%package devel
Summary:        Development files for libpng
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       zlib-devel%{?_isa}

%description devel
Headers, configuration scripts, unversioned library links, manual pages, and
pkg-config metadata for developing applications with libpng.

%package tools
Summary:        Low-level tools for inspecting and repairing PNG files
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description tools
Low-level pngfix and png-fix-itxt utilities supplied by libpng upstream.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build -j1 check

%files
%license LICENSE
%{_libdir}/libpng16.so.16*

%files devel
%license LICENSE
%doc ANNOUNCE CHANGES README TODO example.c libpng-manual.txt
%{_bindir}/libpng-config
%{_bindir}/libpng16-config
%{_includedir}/libpng16/
%{_includedir}/png.h
%{_includedir}/pngconf.h
%{_includedir}/pnglibconf.h
%{_libdir}/libpng.so
%{_libdir}/libpng16.so
%{_libdir}/pkgconfig/libpng.pc
%{_libdir}/pkgconfig/libpng16.pc
%{_mandir}/man3/libpng.3*
%{_mandir}/man3/libpngpf.3*
%{_mandir}/man5/png.5*

%files tools
%{_bindir}/png-fix-itxt
%{_bindir}/pngfix

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2:1.6.58-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
