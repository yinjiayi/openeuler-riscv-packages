# SPDX-License-Identifier: Apache-2.0
Name:           libwhirlpool
Version:        1.1
Release:        1%{?dist}
Summary:        Whirlpool hash library and checksum utility
License:        LicenseRef-Public-Domain AND Apache-2.0
URL:            https://github.com/dfateyev/libwhirlpool
Source0:        https://codeload.github.com/dfateyev/libwhirlpool/tar.gz/b7721a44275793171c4b8ee17645394d9b5c927e#/libwhirlpool-1.1.tar.gz
Source1:        GPL-2.0.txt
Source2:        GPL-3.0.txt
Source3:        APACHE-2.0.txt
Patch0:         patches/0001-fix-checksum-buffer-terminator.patch
BuildRequires:  gcc make glibc-devel autoconf automake libtool
BuildRequires:  binutils coreutils grep sed

%description
Whirlpool hash implementation, shared and static C library and whirlpoolsum
file-checksum utility. The complete original default build is retained.

%package devel
Summary:        Header, linking libraries and downstream consumer fixture
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc glibc-devel binutils coreutils grep

%description devel
Public header, shared linking interface, static archive and an explicitly
downstream fixed-vector consumer fixture for installed-library verification.

%prep
%setup -q -n libwhirlpool-b7721a44275793171c4b8ee17645394d9b5c927e
%patch -P 0 -p1
cp -p %{SOURCE1} GPL-2.0.txt
cp -p %{SOURCE2} GPL-3.0.txt
cp -p %{SOURCE3} APACHE-2.0.txt
# Separate downstream fixture; original sources and tests are not modified.
cat > consumer.c <<'C'
/* SPDX-License-Identifier: Apache-2.0
 * Empty/abc vector constants: official OpenSSL openssl-3.0.0
 * test/recipes/30-test_evp_data/evpmd_whirlpool.txt, ISO vector set.
 * Copyright 2001-2020 The OpenSSL Project Authors. All Rights Reserved.
 */
#include <stdio.h>
#include <string.h>
#include <whirlpool.h>
static int check(const char *text, const char *expected, unsigned long piece) {
    NESSIEstruct w;
    unsigned char digest[DIGESTBYTES];
    char hex[2 * DIGESTBYTES + 1];
    unsigned long n = (unsigned long)strlen(text), i;
    whirlpool_init(&w);
    for (i = 0; i < n; i += piece) {
        unsigned long take = n - i < piece ? n - i : piece;
        whirlpool_add((unsigned char *)text + i, take * 8, &w);
    }
    whirlpool_finalize(&w, digest);
    for (i = 0; i < DIGESTBYTES; ++i) sprintf(hex + 2 * i, "%%02X", digest[i]);
    if (strcmp(hex, expected) != 0) {
        fprintf(stderr, "downstream vector mismatch piece=%%lu: %%s\n", piece, hex);
        return 1;
    }
    return 0;
}
int main(void) {
    const char *empty = "19FA61D75522A4669B44E39C1D2E1726C530232130D407F89AFEE0964997F7A73E83BE698B288FEBCF88E3E03C4F0757EA8964E59B63D93708B138CC42A66EB3";
    const char *abc = "4E2448A4C6F486BB16B6562C73B4020BF3043E3A731BCE721AE1B303D97E6D4C7181EEBDB6C57E277D0E34957114CBD6C797FC9D95D8B582D225292076D4EEF5";
    if (check("", empty, 1) || check("abc", abc, 1) || check("abc", abc, 2) || check("abc", abc, 3)) return 1;
    puts("PASS downstream-libwhirlpool empty/abc vectors; skips=0");
    return 0;
}
C

%build
%set_build_flags
# Native target compiler inside the locked target; no cross-build test skip.
./configure --prefix=%{_prefix} --libdir=%{_libdir} \
    --includedir=%{_includedir} --bindir=%{_bindir} --mandir=%{_mandir} \
    CC=gcc CFLAGS="%{optflags}" LDFLAGS="$LDFLAGS"
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libwhirlpool.la
install -d %{buildroot}%{_datadir}/libwhirlpool/tests
install -m 0644 consumer.c %{buildroot}%{_datadir}/libwhirlpool/tests/
sha256sum consumer.c > %{buildroot}%{_datadir}/libwhirlpool/tests/SHA256SUMS

%check
# Original make check has no registered suite; retain it and run original API test.
make -j1 check > upstream-check.log 2>&1
cat upstream-check.log
./src/whirlpoolsum --test > upstream-api.log 2>&1
cat upstream-api.log
grep -Fx 'No error detected.' upstream-api.log
if grep -F 'API error' upstream-api.log; then exit 1; fi
gcc %{optflags} -I%{buildroot}%{_includedir} consumer.c \
    -L%{buildroot}%{_libdir} -lwhirlpool -o staged-shared
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./staged-shared
gcc %{optflags} -I%{buildroot}%{_includedir} consumer.c \
    %{buildroot}%{_libdir}/libwhirlpool.a -o staged-static
./staged-static

%files
%license COPYING GPL-2.0.txt GPL-3.0.txt APACHE-2.0.txt install-sh
%doc README AUTHORS NEWS ChangeLog
%{_libdir}/libwhirlpool.so.0
%{_libdir}/libwhirlpool.so.0.0.2
%{_bindir}/whirlpoolsum
%{_mandir}/man1/whirlpoolsum.1*

%files devel
%{_includedir}/whirlpool.h
%{_libdir}/libwhirlpool.so
%{_libdir}/libwhirlpool.a
%{_datadir}/libwhirlpool/

%changelog
* Fri Oct 16 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1-1
- Pin official v1.1; preserve original tests and add downstream installed checks.
