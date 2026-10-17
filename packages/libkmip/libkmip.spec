# SPDX-License-Identifier: Apache-2.0
Name:           libkmip
Version:        0.2.0
Release:        1%{?dist}
Summary:        C11 implementation of the Key Management Interoperability Protocol
License:        Apache-2.0 OR BSD-3-Clause
URL:            https://github.com/OpenKMIP/libkmip
Source0:        libkmip-0.2.0.tar.gz
Patch0:         0001-library-install-link.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel >= 1.1.0
Requires:       gcc
Requires:       openssl-devel >= 1.1.0
Requires:       bash
Requires:       coreutils
Requires:       diffutils

%description
C11 encoding and decoding support for the Key Management Interoperability
Protocol, including OpenSSL BIO helpers. Includes the upstream shared/static
libraries, headers, three example clients, test program, source and RST docs.
This package does not claim security certification or live-server validation.

%prep
%setup -q -n libkmip-5b4e6733215f5f2df0d83a761986c973d7c2abf7
%patch0 -p1

%build
# Keep the original all target: both libraries, three demos and all tests.
%make_build CC=gcc CFLAGS="%{optflags} -std=c11 -pedantic -g3 -Wall -Wextra -UNDEBUG" LDFLAGS="%{?build_ldflags} -L/usr/local/lib"

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} CC=gcc CFLAGS="%{optflags} -std=c11 -pedantic -g3 -Wall -Wextra -UNDEBUG" LDFLAGS="%{?build_ldflags} -L/usr/local/lib"
install -d %{buildroot}%{_datadir}/libkmip
cat > %{buildroot}%{_datadir}/libkmip/consumer.c <<'C'
#include <kmip/kmip.h>
#include <kmip/kmip_bio.h>
#include <kmip/kmip_memset.h>
#include <string.h>
int main(void) {
    const uint8 expected[16] = {0x42,0,0,2,0,0,0,4,0,0,0,8,0,0,0,0};
    uint8 bytes[16] = {0};
    KMIP ctx = {0};
    kmip_init(&ctx, bytes, sizeof(bytes), KMIP_1_0);
    if (kmip_encode_integer(&ctx, KMIP_TAG_DEFAULT, 8) != KMIP_OK ||
        memcmp(bytes, expected, sizeof(bytes)) != 0) return 1;
    kmip_destroy(&ctx);
    memcpy(bytes, expected, sizeof(bytes));
    int32 observed = 0;
    kmip_init(&ctx, bytes, sizeof(bytes), KMIP_1_0);
    if (kmip_decode_integer(&ctx, KMIP_TAG_DEFAULT, &observed) != KMIP_OK || observed != 8) return 2;
    kmip_destroy(&ctx);
    kmip_memset(bytes, 0, sizeof(bytes));
    for (unsigned i=0; i<sizeof(bytes); ++i) if (bytes[i]) return 3;
    BIO *bio = BIO_new(BIO_s_mem());
    if (!bio) return 4;
    BIO_free(bio);
    return 0;
}
C
cat > %{buildroot}%{_datadir}/libkmip/run-tests.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
base="$root/usr/share/libkmip"
(cd "$base"; sha256sum -c SHA256SUMS)
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
export LD_LIBRARY_PATH="$root/usr/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
"$root/usr/bin/kmip/tests" > "$work/installed-tests.log"
cat "$work/installed-tests.log"
grep -Eq '^    FAILURE: 0$' "$work/installed-tests.log"
grep -Eq '^Total tests: 178$' "$work/installed-tests.log"
# Rebuild the entire unchanged upstream suite against installed headers/library.
gcc -std=c11 -pedantic -Wall -Wextra -UNDEBUG -I"$root/usr/include/kmip" \
  "$root/usr/src/kmip/tests.c" -L"$root/usr/lib64" -lkmip -lssl -lcrypto -o "$work/tests"
"$work/tests" > "$work/shared-tests.log"
cat "$work/shared-tests.log"
grep -Eq '^    FAILURE: 0$' "$work/shared-tests.log"
grep -Eq '^Total tests: 178$' "$work/shared-tests.log"
for mode in shared static; do
  library=(-L"$root/usr/lib64" -lkmip)
  if [[ $mode == static ]]; then library=("$root/usr/lib64/libkmip.a"); fi
  gcc -std=c11 -pedantic -Wall -Wextra -UNDEBUG -I"$root/usr/include" \
    "$base/consumer.c" "${library[@]}" -lssl -lcrypto -o "$work/consumer-$mode"
  "$work/consumer-$mode"
done
for demo in demo_create demo_get demo_destroy; do
  "$root/usr/bin/kmip/$demo" -h > "$work/$demo-help.log"
  grep -q '^Usage:' "$work/$demo-help.log"
done
printf 'PASS downstream original-installed-suite=1 original-shared-suite=1 consumers=2 demo-help=3 skips=0\n'
SH
chmod 0755 %{buildroot}%{_datadir}/libkmip/run-tests.sh
(cd %{buildroot}%{_datadir}/libkmip; sha256sum consumer.c) > %{buildroot}%{_datadir}/libkmip/SHA256SUMS

%check
# Unchanged default suite; no live KMIP server/network is required.
make test
bash %{buildroot}%{_datadir}/libkmip/run-tests.sh "%{buildroot}"

%files
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.md CHANGELOG.rst
%{_bindir}/kmip/
%{_includedir}/kmip/
%{_libdir}/libkmip.so*
%{_libdir}/libkmip.a
%{_prefix}/src/kmip/
%{_docdir}/kmip/
%{_datadir}/libkmip/

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.0-1
- Preserve complete original defaults and add installed-library acceptance.
