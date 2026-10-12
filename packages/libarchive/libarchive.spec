# SPDX-License-Identifier: Apache-2.0
Name:           libarchive
Version:        3.8.9
Release:        1%{?dist}
Summary:        Multi-format archive and compression library
License:        BSD-2-Clause AND BSD-4-Clause-UC AND (Apache-2.0 OR CC0-1.0 OR OpenSSL)
URL:            https://libarchive.org/
Source0:        libarchive-%{version}.tar.xz

BuildRequires:  bzip2
BuildRequires:  bzip2-devel
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  gzip
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  libb2-devel
BuildRequires:  libxml2-devel
BuildRequires:  lz4
BuildRequires:  lz4-devel
BuildRequires:  lzip
BuildRequires:  lzo-devel
BuildRequires:  lzop
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconf
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  zstd
BuildRequires:  zstd-devel

%description
libarchive is a streaming library for reading and writing multiple archive
and compression formats. It also provides the bsdtar, bsdcpio, bsdcat, and
bsdunzip command-line tools.

%package devel
Summary:        Development files for libarchive
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, the unversioned shared-library link, pkg-config metadata, and API
manual pages for developing applications with libarchive.

%package help
Summary:        Documentation for libarchive and its command-line tools
BuildArch:      noarch

%description help
Manual pages and additional documentation for libarchive, bsdtar, bsdcpio,
bsdcat, and bsdunzip.

%package -n bsdtar
Summary:        Tar-compatible archiver using libarchive
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdtar
The bsdtar command-line archive utility from libarchive.

%package -n bsdcpio
Summary:        Cpio-compatible archiver using libarchive
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdcpio
The bsdcpio command-line archive utility from libarchive.

%package -n bsdcat
Summary:        Archive decompression filter using libarchive
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdcat
The bsdcat command-line decompression filter from libarchive.

%package -n bsdunzip
Summary:        Zip archive extractor using libarchive
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n bsdunzip
The bsdunzip command-line Zip archive extractor from libarchive.

%prep
%autosetup

%build
%configure \
  --disable-static \
  --enable-shared \
  --enable-bsdtar=shared \
  --enable-bsdcat=shared \
  --enable-bsdcpio=shared \
  --enable-bsdunzip=shared \
  --with-lzo2
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
timeout 60m make -j1 check

%files
%license COPYING
%{_libdir}/libarchive.so.13*

%files devel
%license COPYING
%{_includedir}/archive.h
%{_includedir}/archive_entry.h
%{_libdir}/libarchive.so
%{_libdir}/pkgconfig/libarchive.pc

%files help
%license COPYING
%doc NEWS README.md
%{_mandir}/man3/archive*.3*
%{_mandir}/man3/libarchive*.3*
%{_mandir}/man5/cpio.5*
%{_mandir}/man5/libarchive-formats.5*
%{_mandir}/man5/mtree.5*
%{_mandir}/man5/tar.5*
%{_mandir}/man1/bsdcat.1*
%{_mandir}/man1/bsdcpio.1*
%{_mandir}/man1/bsdtar.1*
%{_mandir}/man1/bsdunzip.1*

%files -n bsdtar
%license COPYING
%{_bindir}/bsdtar

%files -n bsdcpio
%license COPYING
%{_bindir}/bsdcpio

%files -n bsdcat
%license COPYING
%{_bindir}/bsdcat

%files -n bsdunzip
%license COPYING
%{_bindir}/bsdunzip

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8.9-1
- Initial openEuler RISC-V package with the complete upstream check suite.
