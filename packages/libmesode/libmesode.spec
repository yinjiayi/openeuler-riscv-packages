# SPDX-License-Identifier: MIT
Name:           libmesode
Version:        0.10.1
Release:        1%{?dist}
Summary:        Lightweight XMPP client library with OpenSSL support
License:        MIT AND LicenseRef-Public-Domain AND LicenseRef-Patrick-Powell
URL:            https://github.com/boothj5/libmesode
Source0:        libmesode-%{version}.tar.gz
Patch0:         0001-bound-DNS-compression-jumps.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  expat-devel
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  patch
BuildRequires:  pkgconf
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       coreutils

%description
An XMPP client library forked from libstrophe, retaining its distinct libmesode
library, mesode.h header and pkg-config identity. OpenSSL and Expat support,
shared/static libraries and all upstream default checks/examples are preserved.

%prep
%setup -q -n libmesode-%{version}
set -eu
set -o pipefail
# Preserve all 83 original regular members before any generated helper changes.
# .notice suffix prevents RPM configure helper refresh from rewriting originals.
mkdir license-notices
find . -type f ! -path './license-notices/*' -print0 | sort -z |
while IFS= read -r -d '' member; do
    target="license-notices/${member#./}.notice"
    mkdir -p "$(dirname "$target")"
    cp -p "$member" "$target" || exit 1
done
test "$(find license-notices -type f -name '*.notice' | wc -l)" -eq 83
(cd license-notices; find . -type f -name '*.notice' -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)
%autopatch -p1
# Same bootstrap operation as upstream bootstrap.sh; no default feature switches.
mkdir -p m4
autoreconf -fi
cat > api-smoke.c <<'LIBMESODE_API_EOF'
/* SPDX-License-Identifier: MIT */
/* Package-local deterministic API checks; no network or TLS handshake. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <mesode.h>

static void same_text(xmpp_ctx_t *ctx, xmpp_stanza_t *s, const char *expected)
{
    char *text = xmpp_stanza_get_text(s);
    assert(text != NULL && strcmp(text, expected) == 0);
    xmpp_free(ctx, text);
}

int main(void)
{
    xmpp_ctx_t *ctx;
    xmpp_stanza_t *s, *body, *copy, *again, *clone;
    char *wire = NULL, *text, *jid, *part, *encoded, *digest;
    size_t wirelen = 0, decoded_len = 0;
    unsigned char *decoded = NULL;
    static const unsigned char bytes[] = {0x00, 0xff, 0x7f, 0x80};

    xmpp_initialize();
    ctx = xmpp_ctx_new(NULL, NULL);
    assert(ctx != NULL);

    /* 1: XML namespace/ID/entity decoding and malformed input rejection. */
    s = xmpp_stanza_new_from_string(ctx,
        "<message xmlns='jabber:client' id='one'><body>A &amp; B &lt; C</body></message>");
    assert(s != NULL);
    assert(strcmp(xmpp_stanza_get_name(s), "message") == 0);
    assert(strcmp(xmpp_stanza_get_ns(s), XMPP_NS_CLIENT) == 0);
    assert(strcmp(xmpp_stanza_get_id(s), "one") == 0);
    body = xmpp_stanza_get_child_by_name(s, "body");
    assert(body != NULL);
    same_text(ctx, body, "A & B < C");
    assert(xmpp_stanza_new_from_string(ctx, "<") == NULL);
    puts("libmesode API case 1/6: XML parse and malformed rejection");

    /* 2: serializer produces escaped wire; reparse verifies semantic result. */
    assert(xmpp_stanza_set_id(s, "a&b") == XMPP_EOK);
    assert(xmpp_stanza_to_text(s, &wire, &wirelen) == XMPP_EOK);
    assert(wire != NULL && wirelen == strlen(wire));
    assert(strstr(wire, "A &amp; B &lt; C") != NULL);
    assert(strstr(wire, "a&amp;b") != NULL);
    again = xmpp_stanza_new_from_string(ctx, wire);
    assert(again != NULL && strcmp(xmpp_stanza_get_id(again), "a&b") == 0);
    same_text(ctx, xmpp_stanza_get_child_by_name(again, "body"), "A & B < C");
    xmpp_free(ctx, wire);
    assert(xmpp_stanza_release(again) != 0);
    puts("libmesode API case 2/6: escaped XML wire roundtrip");

    /* 3: deep copy has independent attributes/children; clone adds a ref. */
    copy = xmpp_stanza_copy(s);
    assert(copy != NULL && copy != s);
    assert(xmpp_stanza_set_id(copy, "copy") == XMPP_EOK);
    assert(strcmp(xmpp_stanza_get_id(s), "a&b") == 0);
    assert(xmpp_message_set_body(copy, "replacement") == XMPP_EINVOP);
    again = xmpp_stanza_get_child_by_name(copy, "body");
    assert(again != NULL && again != body);
    again = xmpp_stanza_get_children(again);
    assert(again != NULL && xmpp_stanza_is_text(again));
    assert(xmpp_stanza_set_text(again, "replacement") == XMPP_EOK);
    text = xmpp_message_get_body(copy);
    assert(text != NULL && strcmp(text, "replacement") == 0);
    xmpp_free(ctx, text);
    same_text(ctx, body, "A & B < C");
    clone = xmpp_stanza_clone(copy);
    assert(clone == copy);
    assert(xmpp_stanza_release(clone) == 0);
    assert(xmpp_stanza_release(copy) != 0);
    assert(xmpp_stanza_release(s) != 0);
    puts("libmesode API case 3/6: deep-copy and clone ownership");

    /* 4: JID split/new and required-domain failure. */
    jid = xmpp_jid_new(ctx, "alice", "example.invalid", "desktop");
    assert(jid != NULL && strcmp(jid, "alice@example.invalid/desktop") == 0);
    part = xmpp_jid_bare(ctx, jid);
    assert(part != NULL && strcmp(part, "alice@example.invalid") == 0);
    xmpp_free(ctx, part);
    part = xmpp_jid_node(ctx, jid);
    assert(part != NULL && strcmp(part, "alice") == 0);
    xmpp_free(ctx, part);
    part = xmpp_jid_domain(ctx, jid);
    assert(part != NULL && strcmp(part, "example.invalid") == 0);
    xmpp_free(ctx, part);
    part = xmpp_jid_resource(ctx, jid);
    assert(part != NULL && strcmp(part, "desktop") == 0);
    xmpp_free(ctx, part);
    xmpp_free(ctx, jid);
    assert(xmpp_jid_new(ctx, "alice", NULL, "desktop") == NULL);
    puts("libmesode API case 4/6: JID construction and split");

    /* 5: binary Base64 includes NUL/non-ASCII; invalid bytes must fail. */
    encoded = xmpp_base64_encode(ctx, bytes, sizeof(bytes));
    assert(encoded != NULL && strcmp(encoded, "AP9/gA==") == 0);
    xmpp_base64_decode_bin(ctx, encoded, strlen(encoded), &decoded, &decoded_len);
    assert(decoded != NULL && decoded_len == sizeof(bytes));
    assert(memcmp(decoded, bytes, sizeof(bytes)) == 0);
    xmpp_free(ctx, decoded);
    xmpp_free(ctx, encoded);
    decoded = NULL;
    decoded_len = 999;
    xmpp_base64_decode_bin(ctx, "!!!!", 4, &decoded, &decoded_len);
    assert(decoded == NULL && decoded_len == 0);
    puts("libmesode API case 5/6: binary Base64 and invalid rejection");

    /* 6: deterministic SHA1 vector; not a security-strength assertion. */
    digest = xmpp_sha1(ctx, (const unsigned char *)"abc", 3);
    assert(digest != NULL);
    assert(strcmp(digest, "a9993e364706816aba3e25717850c26c9cd0d89d") == 0);
    xmpp_free(ctx, digest);
    puts("libmesode API case 6/6: SHA1 known vector");

    xmpp_ctx_free(ctx);
    xmpp_shutdown();
    puts("libmesode API cases passed: 6/6");
    return 0;
}
LIBMESODE_API_EOF
cat > dns-compression-regression.c <<'LIBMESODE_DNS_EOF'
/*
 * Copyright 2026 openEuler RISC-V package contributors.
 * SPDX-License-Identifier: MIT
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * Target-only deterministic checks. Never compiled or run by local tooling.
 * The positive executable links the actual default static library. Only the
 * separate negative control includes preserved, unmodified original resolver C.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mesode.h"
#include "resolver.h"

#ifdef LIBMESODE_ORIGINAL_NEGATIVE
#include "license-notices/src/resolver.c.notice"
static volatile unsigned decoder_entries;
static volatile int armed;
void __cyg_profile_func_enter(void *, void *) __attribute__((no_instrument_function));
void __cyg_profile_func_exit(void *, void *) __attribute__((no_instrument_function));
void __cyg_profile_func_enter(void *fn, void *caller)
{
    (void)caller;
    if (armed && fn == (void *)message_name_get) {
        ++decoder_entries;
        if (decoder_entries == 65) {
            /* On the fixed self-pointer, every recursive frame gets exactly
             * the same bytes, offset12, NULL destination and SIZE_MAX limit.
             * Stop before uncontrolled stack growth; this is not a timeout.
             */
            fputs("libmesode original compression self-cycle decoder entries=65 EXIT97\n", stderr);
            _Exit(97);
        }
    }
}
void __cyg_profile_func_exit(void *fn, void *caller)
{
    (void)fn;
    (void)caller;
}
#endif

static void header(unsigned char *p, unsigned qd, unsigned an)
{
    memset(p, 0, 12);
    p[2] = 0x80;
    p[4] = (unsigned char)(qd >> 8);
    p[5] = (unsigned char)qd;
    p[6] = (unsigned char)(an >> 8);
    p[7] = (unsigned char)an;
}
static void pointer(unsigned char *p, unsigned offset)
{
    assert(offset < 16384);
    p[0] = (unsigned char)(0xc0 | (offset >> 8));
    p[1] = (unsigned char)offset;
}
static void rejected(xmpp_ctx_t *ctx, const unsigned char *p, size_t size)
{
    resolver_srv_rr_t *rr = (resolver_srv_rr_t *)(uintptr_t)1;
    int rc = resolver_srv_lookup_buf(ctx, p, size, &rr);
    assert(rc == XMPP_DOMAIN_NOT_FOUND && rr == NULL);
}
static void accepted(xmpp_ctx_t *ctx, const unsigned char *p, size_t size,
                     const char *target)
{
    resolver_srv_rr_t *rr = NULL;
    assert(resolver_srv_lookup_buf(ctx, p, size, &rr) == XMPP_DOMAIN_FOUND);
    assert(rr != NULL && rr->next == NULL);
    assert(rr->priority == 1 && rr->weight == 2 && rr->port == 5222);
    assert(strcmp(rr->target, target) == 0);
    resolver_srv_free(ctx, rr);
}
int main(void)
{
    unsigned char p[16384];
    xmpp_ctx_t *ctx;
    setvbuf(stdout, NULL, _IONBF, 0);
    xmpp_initialize();
    ctx = xmpp_ctx_new(NULL, NULL);
    assert(ctx != NULL);
    header(p, 1, 0);
    pointer(p + 12, 12);
    p[14] = 0; p[15] = 33; p[16] = 0; p[17] = 1;
#ifdef LIBMESODE_ORIGINAL_NEGATIVE
    /* Execute only the original self-cycle. No generic pass/failure fallback:
     * expected success for this control is exact97 plus the exact entry marker.
     */
    armed = 1;
    rejected(ctx, p, 18);
    fputs("original self-cycle unexpectedly returned\n", stderr);
    return 1;
#else
    rejected(ctx, p, 18);
    puts("DNS case1 self-cycle rejected");

    header(p, 1, 0);
    pointer(p + 12, 18);
    p[14] = 0; p[15] = 33; p[16] = 0; p[17] = 1;
    pointer(p + 18, 12);
    rejected(ctx, p, 20);
    puts("DNS case2 two-node cycle rejected");

    /* A 4096-pointer acyclic chain ending at the root label remains legal.
     * Its first pointer consumes two bytes; subsequent question fields are
     * followed by a genuine SRV answer. Chain bytes are trailing message data.
     */
    header(p, 1, 1);
    pointer(p + 12, 64);
    p[14] = 0; p[15] = 33; p[16] = 0; p[17] = 1;
    p[18] = 0; /* root owner name */
    p[19] = 0; p[20] = 33; p[21] = 0; p[22] = 1;
    memset(p + 23, 0, 4);
    p[27] = 0; p[28] = 7;
    p[29] = 0; p[30] = 1; p[31] = 0; p[32] = 2;
    p[33] = 0x14; p[34] = 0x66; p[35] = 0;
    for (unsigned i = 0; i < 4095; ++i) pointer(p + 64 + 2 * i, 64 + 2 * (i + 1));
    p[64 + 2 * 4095] = 0;
    accepted(ctx, p, 64 + 2 * 4095 + 1, "");
    puts("DNS case3 long acyclic compression chain accepted");
    pointer(p + 64 + 2 * 4094, 64);
    rejected(ctx, p, 64 + 2 * 4095 + 1);
    puts("DNS case4 long compression cycle rejected");

    header(p, 1, 0);
    p[12] = 0xc0;
    rejected(ctx, p, 13);
    pointer(p + 12, 16383);
    rejected(ctx, p, 18);
    p[12] = 3; p[13] = 'a';
    rejected(ctx, p, 14);
    p[12] = 0x40;
    rejected(ctx, p, 18);
    puts("DNS case5 truncated pointer label out-of-range and reserved forms rejected");

    /* Question a.example; compressed answer owner and target b.example. */
    header(p, 1, 1);
    p[12] = 1; p[13] = 'a'; p[14] = 7;
    memcpy(p + 15, "example", 7); p[22] = 0;
    p[23] = 0; p[24] = 33; p[25] = 0; p[26] = 1;
    pointer(p + 27, 12);
    p[29] = 0; p[30] = 33; p[31] = 0; p[32] = 1;
    memset(p + 33, 0, 4);
    p[37] = 0; p[38] = 10;
    p[39] = 0; p[40] = 1; p[41] = 0; p[42] = 2;
    p[43] = 0x14; p[44] = 0x66;
    p[45] = 1; p[46] = 'b'; pointer(p + 47, 14);
    accepted(ctx, p, 49, "b.example");
    puts("DNS case6 legitimate compressed owner and target accepted");
    xmpp_ctx_free(ctx);
    xmpp_shutdown();
    puts("libmesode DNS compression regression cases 6/6 PASS");
    return 0;
#endif
}
LIBMESODE_DNS_EOF

%build
%configure --enable-shared --enable-static CFLAGS="%{optflags} -UNDEBUG"
%make_build
gcc %{optflags} -UNDEBUG -I. api-smoke.c -L.libs -lmesode \
    $(pkg-config --libs openssl expat) -lresolv %{?__global_ldflags} -o api-smoke

%install
%make_install
rm -f %{buildroot}%{_libdir}/libmesode.la
install -d %{buildroot}%{_libexecdir}/libmesode-tests
install -m 0755 api-smoke %{buildroot}%{_libexecdir}/libmesode-tests/api-smoke
install -m 0644 api-smoke.c %{buildroot}%{_libexecdir}/libmesode-tests/api-smoke.c
(cd %{buildroot}%{_libexecdir}/libmesode-tests; sha256sum api-smoke.c > SHA256SUMS)

%check
# Original default make check runs all twelve TESTS without omissions or retries.
%make_build check
grep -Eq '^# TOTAL: +12$' test-suite.log
grep -Eq '^# PASS: +12$' test-suite.log
grep -Eq '^# SKIP: +0$' test-suite.log
grep -Eq '^# FAIL: +0$' test-suite.log
grep -Eq '^# ERROR: +0$' test-suite.log
for example in active basic bot component roster uuid vcard; do
    test -x "examples/$example"
done
(cd license-notices; sha256sum -c SHA256SUMS)
LD_LIBRARY_PATH="$PWD/.libs" ./api-smoke
# Supplemental deterministic target-only decoder regression. Original tests above
# remain byte-for-byte unchanged; original source control is separately linked.
set -eu
mkdir dns-compression-results
gcc %{optflags} -UNDEBUG -I. -Isrc dns-compression-regression.c \
    .libs/libmesode.a $(pkg-config --libs openssl expat) -lresolv \
    %{?__global_ldflags} -o dns-compression-patched
gcc %{optflags} -UNDEBUG -I. -Isrc -DLIBMESODE_ORIGINAL_NEGATIVE \
    -finstrument-functions dns-compression-regression.c .libs/libmesode.a \
    $(pkg-config --libs openssl expat) -lresolv %{?__global_ldflags} \
    -o dns-compression-original
set +x
if ./dns-compression-original > dns-compression-results/original.stdout 2> dns-compression-results/original.stderr; then original_status=0; else original_status=$?; fi
if ./dns-compression-patched > dns-compression-results/patched.stdout 2> dns-compression-results/patched.stderr; then patched_status=0; else patched_status=$?; fi
printf '%%s\n' "$original_status" > dns-compression-results/original.exit
printf '%%s\n' "$patched_status" > dns-compression-results/patched.exit
sha256sum dns-compression-regression.c src/resolver.c license-notices/src/resolver.c.notice dns-compression-patched dns-compression-original dns-compression-results/*
cat dns-compression-results/original.stderr dns-compression-results/patched.stdout
test "$original_status" -eq 97
test "$patched_status" -eq 0
test ! -s dns-compression-results/original.stdout
test ! -s dns-compression-results/patched.stderr
test "$(wc -l < dns-compression-results/original.stderr)" -eq 1
grep -Fx 'libmesode original compression self-cycle decoder entries=65 EXIT97' dns-compression-results/original.stderr
test "$(wc -l < dns-compression-results/patched.stdout)" -eq 7
grep -Fx 'libmesode DNS compression regression cases 6/6 PASS' dns-compression-results/patched.stdout
set -x

%files
%license LICENSE.txt MIT-LICENSE.txt GPL-LICENSE.txt COPYING license-notices
%doc README.markdown AUTHORS ChangeLog NEWS examples/README.md dns-compression-regression.c
%{_libdir}/libmesode.so.0
%{_libdir}/libmesode.so.0.0.0
%{_libdir}/libmesode.so
%{_libdir}/libmesode.a
%{_includedir}/mesode.h
%{_libdir}/pkgconfig/libmesode.pc
%{_libexecdir}/libmesode-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10.1-1
- Preserve official default TLS, Expat, shared/static, twelve checks and seven examples.
- Retain all original notices and add six deterministic installed-library API cases.
