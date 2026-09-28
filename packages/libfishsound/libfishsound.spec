# SPDX-License-Identifier: Apache-2.0
Name:           libfishsound
Version:        1.0.1
Release:        1%{?dist}
Summary:        Simple audio encode and decode API for Xiph codecs
License:        BSD-3-Clause
URL:            https://xiph.org/fishsound/
Source0:        libfishsound-%{version}.tar.gz

BuildRequires:  flac-devel
BuildRequires:  gcc
BuildRequires:  libogg-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libvorbis-devel
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  speex-devel

%description
Libfishsound provides a common API for encoding and decoding Vorbis, Speex,
and FLAC audio streams.

%package devel
Summary:        Development files for Libfishsound
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       flac-devel%{?_isa}
Requires:       libvorbis-devel%{?_isa}
Requires:       pkgconf
Requires:       speex-devel%{?_isa}

%description devel
Public headers, linker name, and pkg-config metadata for Libfishsound.

%prep
%autosetup -p1

%build
%configure --disable-static
grep -Eq '^#define HAVE_VORBIS 1$' config.h
grep -Eq '^#define HAVE_SPEEX 1$' config.h
grep -Eq '^#define HAVE_FLAC 1$' config.h
grep -Eq '^#define FS_ENCODE 1$' config.h
grep -Eq '^#define FS_DECODE 1$' config.h
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build -j1 check

%files
%license COPYING
%doc README
%{_libdir}/libfishsound.so.1*
%{_docdir}/libfishsound/html/

%files devel
%license COPYING
%{_includedir}/fishsound/
%{_libdir}/libfishsound.so
%{_libdir}/pkgconfig/fishsound.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Package the official Libfishsound 1.0.1 release for openEuler RISC-V.
