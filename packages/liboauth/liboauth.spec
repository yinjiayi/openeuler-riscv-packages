# SPDX-License-Identifier: Apache-2.0
Name:           liboauth
Version:        1.0.3
Release:        4%{?dist}
%global upstream_commit 07fc30bf6d44f5b431a943452f6083fbaf22bc8f
Summary:        C library for OAuth request signing
License:        MIT
URL:            https://github.com/x42/liboauth
Source0:        liboauth-%{version}.tar.gz
Patch0:         0001-openssl-3-allocate-evp-digest-contexts.patch
Patch1:         0002-public-header-include-size-t-definition.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libcurl-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconf

%description
liboauth supplies URL encoding, request signing, and signature verification
functions for OAuth clients and servers. This build includes libcurl HTTP
integration and OpenSSL-backed cryptographic signatures.

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
%configure --disable-static
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
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-4
- Make the public header self-contained for installed development consumers.

* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-3
- Use upstream's complete OpenSSL crypto backend with OpenSSL 3 context
  lifecycle compatibility; retain all three upstream self-tests.
- The target NSS backend rejected RSA-SHA1 with
  SEC_ERROR_SIGNATURE_ALGORITHM_DISABLED; do not weaken system policy.

* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-2
- Preserve all upstream tests while reporting NSS RSA signing failures as
  explicit tcwiki assertion failures instead of a segmentation fault.

* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package with all three offline upstream self-tests.
