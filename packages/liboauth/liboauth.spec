# SPDX-License-Identifier: Apache-2.0
Name:           liboauth
Version:        1.0.3
Release:        1%{?dist}
%global upstream_commit 07fc30bf6d44f5b431a943452f6083fbaf22bc8f
Summary:        C library for OAuth request signing
License:        MIT
URL:            https://github.com/x42/liboauth
Source0:        liboauth-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libcurl-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  nss-devel
BuildRequires:  pkgconf

%description
liboauth supplies URL encoding, request signing, and signature verification
functions for OAuth clients and servers. This build includes libcurl HTTP
integration and NSS-backed cryptographic signatures.

%package devel
Summary:        Development files for liboauth
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
The public header, unversioned linker name, and pkg-config metadata for
applications using liboauth.

%prep
%autosetup -n liboauth-%{upstream_commit} -p1

%build
autoreconf -fi
%configure --disable-static --enable-nss
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# All three registered upstream TESTS are self-contained and offline.
# Retain per-case progress on a crash so the CI artifact identifies the
# failing assertion rather than only reporting the harness exit status.
if ! %make_build check TESTS_ENVIRONMENT='stdbuf -oL -eL'; then
    test -f test-suite.log && sed -n '1,240p' test-suite.log
    exit 1
fi

%files
%license COPYING.MIT
%doc AUTHORS ChangeLog README
%{_libdir}/liboauth.so.0*
%{_mandir}/man3/oauth.3*

%files devel
%license COPYING.MIT
%{_includedir}/oauth.h
%{_libdir}/liboauth.so
%{_libdir}/pkgconfig/oauth.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package with all three offline upstream self-tests.
