# SPDX-License-Identifier: MIT
Name:           libmesode
Version:        0.10.1
Release:        1%{?dist}
Summary:        Lightweight XMPP client library with OpenSSL support
License:        MIT AND LicenseRef-Public-Domain AND LicenseRef-Patrick-Powell
URL:            https://github.com/boothj5/libmesode
Source0:        libmesode-%{version}.tar.gz
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
%autosetup -n libmesode-%{version} -p1
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

%files
%license LICENSE.txt MIT-LICENSE.txt GPL-LICENSE.txt COPYING license-notices
%doc README.markdown AUTHORS ChangeLog NEWS examples/README.md
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
