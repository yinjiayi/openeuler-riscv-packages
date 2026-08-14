# SPDX-License-Identifier: Apache-2.0
Name:           xz
Version:        5.8.3
Release:        1%{?dist}
Summary:        LZMA compression utilities and library
License:        0BSD AND GPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-or-later
URL:            https://tukaani.org/xz/
Source0:        xz-%{version}.tar.xz

BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  make
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       grep

%description
XZ Utils provides command-line tools and the liblzma library for lossless
compression using the LZMA and XZ formats.

%package libs
Summary:        Runtime library for XZ compression
License:        0BSD

%description libs
The liblzma shared library used to encode and decode XZ and LZMA streams.

%package devel
Summary:        Development files for liblzma
License:        0BSD
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

%description devel
Headers, static and unversioned libraries, and pkg-config metadata for
developing applications with liblzma.

%package lzma-compat
Summary:        Compatibility tools for the legacy LZMA format
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       lzma = %{version}
Obsoletes:      lzma < %{version}

%description lzma-compat
Compatibility command names for reading and writing the legacy LZMA format.

%package help
Summary:        Documentation and translations for XZ Utils
BuildArch:      noarch

%description help
Manual pages, translated messages, and installed documentation for XZ Utils.

%prep
%autosetup -p1

%build
%configure \
  --disable-silent-rules \
  --docdir=%{_docdir}/%{name}
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/liblzma.la

%check
%make_build check

%files
%license COPYING COPYING.0BSD COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1
%{_bindir}/unxz
%{_bindir}/xz*

%files libs
%license COPYING COPYING.0BSD
%{_libdir}/liblzma.so.5*

%files devel
%license COPYING COPYING.0BSD
%{_includedir}/lzma.h
%{_includedir}/lzma/
%{_libdir}/liblzma.a
%{_libdir}/liblzma.so
%{_libdir}/pkgconfig/liblzma.pc

%files lzma-compat
%license COPYING COPYING.0BSD COPYING.GPLv2
%{_bindir}/lz*
%{_bindir}/unlzma

%files help
%license COPYING COPYING.0BSD COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1
%{_docdir}/%{name}/
%{_mandir}/man1/*
%{_mandir}/*/man1/*
%{_datadir}/locale/*/LC_MESSAGES/xz.mo

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.8.3-1
- Initial openEuler RISC-V package from reviewed Fedora 44 and upstream evidence.
- Match the upstream 5.8.3 documentation payload, which has no Texinfo manual.
