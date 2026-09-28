# SPDX-License-Identifier: Apache-2.0
Name:           libmicrohttpd
Version:        1.0.10
Release:        1%{?dist}
Summary:        Embedded HTTP and HTTPS server library
License:        LGPL-2.1-or-later
URL:            https://www.gnu.org/software/libmicrohttpd/
Source0:        libmicrohttpd-%{version}.tar.gz

BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  gnutls-devel
BuildRequires:  libcurl-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  texinfo

%description
GNU libmicrohttpd embeds an HTTP/1.1 and HTTPS server in C applications.
This build retains GnuTLS support and the upstream default functional tests.

%package devel
Summary:        Headers and pkg-config metadata for libmicrohttpd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public header, linker name, and pkg-config metadata for applications
that embed GNU libmicrohttpd.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-https=yes \
  --with-gnutls=yes \
  --enable-curl=yes
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete
# install-info creates a directory index for the buildroot, not this package.
rm -f %{buildroot}%{_infodir}/dir

%check
# Keep the full upstream default functional suite, including libcurl and TLS.
# The optional heavy timing/performance suite requires a dedicated native host.
make check
test -x src/testcurl/test_get
test -x src/testcurl/https/test_https_get_select

%files
%license COPYING
%doc ChangeLog README
%{_libdir}/libmicrohttpd.so.12*
%{_mandir}/man3/libmicrohttpd.3*
%{_infodir}/libmicrohttpd*.info*
%{_infodir}/libmicrohttpd_performance_data.png*

%files devel
%license COPYING
%{_includedir}/microhttpd.h
%{_libdir}/libmicrohttpd.so
%{_libdir}/pkgconfig/libmicrohttpd.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.10-1
- Initial package from the official stable release with HTTPS tests enabled.
