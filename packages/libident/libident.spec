# SPDX-License-Identifier: Apache-2.0
Name:           libident
Version:        0.32
Release:        1%{?dist}
Summary:        RFC1413 Ident client library
License:        LicenseRef-libident AND FSFULLR AND MIT AND GPL-2.0-or-later AND ISC
URL:            https://www.remlab.net/libident/
Source0:        libident-0.32.tar.bz2
Source1:        gpl-2.0.txt
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
An RFC1413 Ident client library with low-level query/reply and higher-level
lookup interfaces, shared/static libraries, public header and manual page.

%prep
%autosetup -n libident-%{version} -p1
cp %{SOURCE1} COPYING.GPL2
# Preserve every original source/notice before standard regeneration.
mkdir license-notices
for notice_file in *; do
    case "$notice_file" in
        license-notices) ;;
        *) cp -a "$notice_file" license-notices/ ;;
    esac
done
# Hash the original 32 members and auxiliary GPL2 text before regeneration.
(
    cd license-notices
    for notice_file in * admin/*; do
        if test -f "$notice_file"; then
            sha256sum "$notice_file"
        fi
    done
) > original-notices.sha256
mv original-notices.sha256 license-notices/SHA256SUMS
# Target configure macros recursively rewrite these exact basenames. Protect
# only the inert notice copies; active build helpers still get target updates.
for notice_file in config.guess config.sub ltmain.sh; do
    mv "license-notices/admin/$notice_file" "license-notices/admin/$notice_file.original"
done
# Target-supplied current Autotools provide riscv64 configuration helpers.
autoreconf -fi

%build
# Preserve shared/static=yes, debug=false and optional testers=false defaults.
%configure
%make_build
# Additional packaging driver: only local sockets/parsing, no live server.
cat > api-smoke.c <<'EOF'
/* SPDX-License-Identifier: ISC
 * Copyright (c) 2026 openEuler RISC-V packaging contributors
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */
#include <ident.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

static void reply_case(const char *reply, int expected_rc,
                       const char *expected_user, const char *expected_os,
                       const char *expected_charset)
{
    int pair[2], local_port = -1, far_port = -1, rc;
    ident_t id;
    char *user = NULL, *os = NULL, *charset = NULL;
    memset(&id, 0, sizeof id);
    assert(socketpair(AF_UNIX, SOCK_STREAM, 0, pair) == 0);
    id.fd = pair[0];
    assert(write(pair[1], reply, strlen(reply)) == (ssize_t)strlen(reply));
    assert(shutdown(pair[1], SHUT_WR) == 0);
    rc = id_parse(&id, NULL, &local_port, &far_port, &user, &os, &charset);
    assert(rc == expected_rc);
    if (expected_rc == 1 || expected_rc == 2 || expected_rc == -3) {
        assert(local_port == 123 && far_port == 456);
    }
    assert((expected_user == NULL && user == NULL) ||
           (expected_user != NULL && user != NULL && strcmp(user, expected_user) == 0));
    assert((expected_os == NULL && os == NULL) ||
           (expected_os != NULL && os != NULL && strcmp(os, expected_os) == 0));
    assert((expected_charset == NULL && charset == NULL) ||
           (expected_charset != NULL && charset != NULL && strcmp(charset, expected_charset) == 0));
    free(user); free(os); free(charset);
    assert(close(pair[0]) == 0 && close(pair[1]) == 0);
}

int main(void)
{
    int pair[2];
    ident_t id;
    char query[64] = {0};
    const char *expected_query = "123 , 456\r\n";
    assert(strcmp(id_version, "0.32") == 0);
    reply_case("123 , 456 : USERID : UNIX , UTF-8 : alice\r\n",
               1, "alice", "UNIX", "UTF-8");
    reply_case("123 , 456 : USERID : UNIX : bob\n", 1, "bob", "UNIX", NULL);
    reply_case("123 , 456 : ERROR : NO-USER\n", 2, "NO-USER", NULL, NULL);
    reply_case("nonsense\n", -2, "nonsense", NULL, NULL);
    reply_case("123 , 456 : UNKNOWN : value\n", -3, "UNKNOWN", NULL, NULL);
    memset(&id, 0, sizeof id);
    assert(socketpair(AF_UNIX, SOCK_STREAM, 0, pair) == 0);
    id.fd = pair[0];
    assert(id_query(&id, 123, 456, NULL) == (int)strlen(expected_query));
    assert(read(pair[1], query, sizeof query - 1) == (ssize_t)strlen(expected_query));
    assert(strcmp(query, expected_query) == 0);
    assert(close(pair[0]) == 0 && close(pair[1]) == 0);
    ident_free(NULL);
    puts("libident api-smoke: 6 cases passed; version 0.32");
    return 0;
}
EOF
cp api-smoke.c license-notices/
gcc %{optflags} -UNDEBUG -I. api-smoke.c -L.libs -lident \
    %{?build_ldflags} -o api-smoke

%install
%make_install
# Configure has finished; restore original names before the later license copy.
for notice_file in config.guess config.sub ltmain.sh; do
    mv "license-notices/admin/$notice_file.original" "license-notices/admin/$notice_file"
done
# Libtool .la metadata is not an API or an upstream feature.
rm -f %{buildroot}%{_libdir}/libident.la
install -Dm755 api-smoke %{buildroot}%{_libexecdir}/libident-tests/api-smoke

%check
set -eu
export LC_ALL=C
(
    cd license-notices
    sha256sum -c SHA256SUMS
)
# Original check target has no declared TESTS/check_PROGRAMS; do not invent any.
%make_build check
LD_LIBRARY_PATH="$PWD/.libs" ./api-smoke
test -x %{buildroot}%{_libexecdir}/libident-tests/api-smoke
(
    cd %{buildroot}%{_libexecdir}/libident-tests
    sha256sum api-smoke > SHA256SUMS
)

%files
%license COPYING AUTHORS COPYING.GPL2 license-notices
%doc README NEWS ChangeLog
%{_libdir}/libident.so
%{_libdir}/libident.so.0
%{_libdir}/libident.so.0.0.0
%{_libdir}/libident.a
%{_includedir}/ident.h
%{_mandir}/man3/ident.3*
%{_libexecdir}/libident-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.32-1
- Protect original notice copies from recursive configure helper rewriting.
- Preserve upstream defaults and check target; add installed local API checks.
