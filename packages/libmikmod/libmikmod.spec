# SPDX-License-Identifier: Apache-2.0
Name:           libmikmod
Version:        3.3.13
Release:        1%{?dist}
Summary:        Library for playing tracker module music files
License:        GPL-2.0-only AND LicenseRef-Callaway-LGPLv2+
URL:            https://mikmod.sourceforge.net/
Source0:        libmikmod-%{version}.tar.gz

BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pulseaudio-libs-devel

%description
libmikmod is a portable library for playing tracker module formats including
MOD, STM, S3M, MTM, XM, ULT, and IT.

%package devel
Summary:        Development files for libmikmod
Provides:       mikmod-devel = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pulseaudio-libs-devel%{?_isa}

%description devel
Header, configuration helper, unversioned shared-library link, and metadata
for developing applications with libmikmod.

%prep
%autosetup -p1

%build
autoreconf -fiv
%configure \
  --enable-dl \
  --enable-alsa \
  --enable-pulseaudio \
  --disable-simd
%make_build

%install
%make_install INSTALL="install -p"
rm -f %{buildroot}%{_infodir}/dir
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING.LIB COPYING.LESSER
%doc AUTHORS NEWS README TODO
%{_libdir}/libmikmod.so.3*

%files devel
%{_bindir}/libmikmod-config
%{_includedir}/mikmod.h
%{_libdir}/libmikmod.so
%{_libdir}/pkgconfig/libmikmod.pc
%{_datadir}/aclocal/libmikmod.m4
%{_infodir}/mikmod.info*
%{_mandir}/man1/libmikmod-config.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.3.13-1
- Initial openEuler RISC-V package from Fedora 44 and frozen cross-distribution evidence.
