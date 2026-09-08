# SPDX-License-Identifier: Apache-2.0
Name:           libjwt
Version:        3.6.1
Release:        1%{?dist}
Summary:        C library for JSON Web Tokens, JWK, and JWKS
License:        MPL-2.0
URL:            https://libjwt.io
Source0:        libjwt-%{version}.tar.xz

BuildRequires:  bats
BuildRequires:  check-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  jansson-devel
BuildRequires:  jq
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pkgconf

%description
libjwt is a C library for creating, parsing, signing, and validating JSON Web
Tokens, JSON Web Keys, and JSON Web Key Sets.

%package devel
Summary:        Development files for libjwt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, and the unversioned shared library
link for developing applications with libjwt.

%prep
%autosetup -p1

%build
%cmake_conf \
  -DCMAKE_DISABLE_FIND_PACKAGE_Doxygen=ON \
  -DENABLE_COVERAGE=OFF \
  -DWITH_GNUTLS=OFF \
  -DWITH_JSON_C=OFF \
  -DWITH_KCAPI_MD=OFF \
  -DWITH_LIBCURL=OFF \
  -DWITH_MBEDTLS=OFF \
  -DWITH_ML_DSA=OFF \
  -DWITH_OPENSSL=ON \
  -DWITH_TESTS=ON
%cmake_build

%install
%cmake_install
rm -f %{buildroot}%{_libdir}/libjwt.a
rm -rf %{buildroot}%{_docdir}/LibJWT

%check
# Run all 40 registered unit, security, JWE/JWS, JWKS, and Bats CLI tests.
%ctest

%files
%license LICENSE
%doc README.md SECURITY.md
%{_bindir}/jwe-decrypt
%{_bindir}/jwe-encrypt
%{_bindir}/jwk2key
%{_bindir}/jwt-generate
%{_bindir}/jwt-verify
%{_bindir}/key2jwk
%{_libdir}/libjwt.so.14*
%{_mandir}/man1/jwe-decrypt.1*
%{_mandir}/man1/jwe-encrypt.1*
%{_mandir}/man1/jwk2key.1*
%{_mandir}/man1/jwt-generate.1*
%{_mandir}/man1/jwt-verify.1*
%{_mandir}/man1/key2jwk.1*

%files devel
%license LICENSE
%{_includedir}/jwt.h
%{_includedir}/jwt_export.h
%{_libdir}/cmake/LibJWT/
%{_libdir}/libjwt.so
%{_libdir}/pkgconfig/libjwt.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.6.1-1
- Initial openEuler RISC-V package with all 40 registered upstream tests.
