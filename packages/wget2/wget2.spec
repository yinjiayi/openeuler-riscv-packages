# SPDX-License-Identifier: Apache-2.0
Name:           wget2
Version:        2.2.1
Release:        2%{?dist}
Summary:        Modern non-interactive network downloader
License:        GPL-3.0-or-later AND LGPL-3.0-or-later AND GFDL-1.3-or-later
URL:            https://gitlab.com/gnuwget/wget2
Source0:        wget2-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  brotli-devel
BuildRequires:  bzip2-devel
BuildRequires:  ca-certificates
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnutls-devel
BuildRequires:  gpgme-devel
BuildRequires:  libidn2-devel
BuildRequires:  libmicrohttpd-devel
BuildRequires:  libnghttp2-devel
BuildRequires:  libproxy-devel
BuildRequires:  libpsl-devel
BuildRequires:  libtool
BuildRequires:  libunistring-devel
BuildRequires:  make
BuildRequires:  pcre2-devel
BuildRequires:  pkgconf
BuildRequires:  python3
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  zstd-devel

%description
GNU Wget2 is a non-interactive network downloader and successor to GNU Wget.
It supports HTTP/2, compression, internationalized names, signatures, and
parallel transfers through the reusable libwget library.

%package -n wget2-libs
Summary:        Runtime library for GNU Wget2

%description -n wget2-libs
The shared libwget runtime library used by GNU Wget2 and other applications.

%package -n wget2-devel
Summary:        Development files for libwget
Requires:       wget2-libs%{?_isa} = %{version}-%{release}

%description -n wget2-devel
Headers, the unversioned shared-library link, pkg-config metadata, and API
manual pages for developing applications with libwget.

%prep
%autosetup

%build
%configure \
  --disable-static \
  --enable-shared \
  --disable-doc \
  --enable-libproxy \
  --with-ssl=gnutls \
  --with-bzip2 \
  --with-lzma \
  --without-libhsts \
  --without-lzip
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -d \
  %{buildroot}%{_mandir}/man1 \
  %{buildroot}%{_mandir}/man3
install -m 0644 docs/man/man1/wget2.1 \
  %{buildroot}%{_mandir}/man1/wget2.1
install -m 0644 docs/man/man3/libwget-*.3 \
  %{buildroot}%{_mandir}/man3/
%find_lang %{name}

%check
timeout 60m make -j1 check || {
  cat tests/test-suite.log
  exit 1
}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README.md
%{_bindir}/wget2

%files -n wget2-libs
%license COPYING.LESSER
%{_libdir}/libwget.so.4*

%files -n wget2-devel
%license COPYING.LESSER
%{_includedir}/wget.h
%{_includedir}/wgetver.h
%{_libdir}/libwget.so
%{_libdir}/pkgconfig/libwget.pc
%{_mandir}/man3/libwget-*.3*

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-2
- Preserve the complete test suite and emit its diagnostic log on failure.

* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.1-1
- Initial openEuler RISC-V package with the complete upstream check suite.
