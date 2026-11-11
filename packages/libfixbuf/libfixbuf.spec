# SPDX-License-Identifier: Apache-2.0
Name:           libfixbuf
Version:        2.5.4
Release:        1%{?dist}
Summary:        IPFIX message format implementation library
License:        LGPL-3.0-only AND MIT AND X11 AND FSFAP AND FSFULLR AND CC0-1.0 AND (GPL-2.0-or-later WITH Autoconf-exception-generic) AND (GPL-3.0-or-later WITH Autoconf-exception-generic) AND (GPL-2.0-or-later WITH Libtool-exception) AND ISC
URL:            https://tools.netsa.cert.org/fixbuf2/
Source0:        libfixbuf-2.5.4.tar.gz
Source1:        gpl-2.0.txt
Source2:        gpl-3.0.txt
Source3:        CC0-1.0.txt
Source4:        iana-registry-licensing.html
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  glib2-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Implementation of IPFIX message encoding, information models, templates,
collection, and export. This package preserves upstream's default feature
configuration and adds a deterministic userspace API regression driver.

%prep
%autosetup -p1
# Preserve every original archive member before configure can update active
# helper basenames. Inert suffixes prevent recursive macro helper replacement.
find . -path ./license-notices -prune -o -type f -print | while IFS= read -r original; do
    mkdir -p "license-notices/$(dirname "$original")"
    cp -p "$original" "license-notices/$original.notice"
done
cp -p %{SOURCE1} license-notices/GPL-2.0.txt
cp -p %{SOURCE2} license-notices/GPL-3.0.txt
cp -p %{SOURCE3} license-notices/CC0-1.0.txt
cp -p %{SOURCE4} license-notices/IANA-REGISTRY-LICENSING.html
(cd license-notices; find . -type f -print | LC_ALL=C sort | xargs sha256sum) > original-notices.sha256
mv original-notices.sha256 license-notices/SHA256SUMS
find license-notices -type f -exec chmod 0644 {} +
test "$(find license-notices -type f | wc -l)" -eq 124
cat > api-smoke.c <<'LIBFIXBUF_API_EOF'
/*
 * Copyright 2026 openEuler RISC-V package contributors.
 * SPDX-License-Identifier: ISC
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
 * OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
 * CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */
#include <fixbuf/public.h>
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
static fbTemplate_t *template_for(fbInfoModel_t *m) {
    GError *err = NULL;
    fbInfoElementSpec_t fields[] = {
        {"sourceIPv4Address", 4, 0}, {"destinationIPv4Address", 4, 0},
        FB_IESPEC_NULL
    };
    fbTemplate_t *t = fbTemplateAlloc(m);
    assert(t != NULL);
    assert(fbTemplateAppendSpecArray(t, fields, 0, &err));
    assert(err == NULL);
    return t;
}
int main(void) {
    assert(setvbuf(stdout, NULL, _IONBF, 0) == 0);
    GError *err = NULL;
    uint8_t wire[4096] = {0};
    uint8_t stream[sizeof(wire) * 2] = {0};
    uint32_t in[2] = {0x0a000001, 0xc0000201}, out[2] = {0, 0};
    const uint8_t expected[8] = {10, 0, 0, 1, 192, 0, 2, 1};
    fbInfoModel_t *model = fbInfoModelAlloc();
    assert(model != NULL && fbInfoModelCountElements(model) > 100);
    assert(fbInfoModelGetElementByName(model, "sourceIPv4Address") != NULL);
    assert(fbInfoModelGetElementByName(model, "notAnInformationElement") == NULL);
    puts("API case1 information-model PASS");
    fbTemplate_t *t = template_for(model);
    assert(fbTemplateCountElements(t) == 2);
    assert(fbTemplateGetIELenOfMemBuffer(t) == sizeof(in));
    puts("API case2 template-layout PASS");
    fbSession_t *s = fbSessionAlloc(model);
    assert(s != NULL);
    fbSessionSetDomain(s, 0x12345);
    assert(fbSessionGetDomain(s) == 0x12345);
    assert(fbSessionAddTemplate(s, TRUE, 256, t, &err) == 256);
    assert(fbSessionAddTemplate(s, FALSE, 257, t, &err) == 257);
    assert(err == NULL);
    puts("API case3 session-template-domain PASS");
    fbExporter_t *exp = fbExporterAllocBuffer(wire, sizeof(wire));
    assert(exp != NULL);
    fBuf_t *writer = fBufAllocForExport(s, exp);
    assert(writer != NULL);
    fBufSetExportTime(writer, 1700000000);
    assert(fbSessionExportTemplates(s, &err));
    /* Buffer exporters replace buf[0] on each emit, rather than append.
     * Preserve the complete template message before emitting the data. */
    assert(fBufEmit(writer, &err));
    assert(err == NULL);
    size_t template_len = fbExporterGetMsgLen(exp);
    assert(template_len == 32 && template_len <= sizeof(wire));
    assert(wire[0] == 0 && wire[1] == 10);
    assert((((size_t)wire[2] << 8) | wire[3]) == template_len);
    assert(wire[12] == 0 && wire[13] == 1 && wire[14] == 0x23 && wire[15] == 0x45);
    assert(wire[16] == 0 && wire[17] == 2);  /* Template Set */
    assert(wire[18] == 0 && wire[19] == 16);
    assert(wire[20] == 1 && wire[21] == 1);  /* Template 257 */
    assert(wire[22] == 0 && wire[23] == 2);  /* Two fields */
    assert(wire[24] == 0 && wire[25] == 8 && wire[26] == 0 && wire[27] == 4);
    assert(wire[28] == 0 && wire[29] == 12 && wire[30] == 0 && wire[31] == 4);
    memcpy(stream, wire, template_len);
    assert(fBufSetInternalTemplate(writer, 256, &err));
    assert(fBufSetExportTemplate(writer, 257, &err));
    assert(fBufAppend(writer, (uint8_t *)in, sizeof(in), &err));
    assert(fBufEmit(writer, &err));
    assert(err == NULL);
    size_t len = fbExporterGetMsgLen(exp);
    assert(len > 24 && len <= sizeof(wire));
    assert(wire[0] == 0 && wire[1] == 10);
    assert((((size_t)wire[2] << 8) | wire[3]) == len);
    assert(wire[12] == 0 && wire[13] == 1 && wire[14] == 0x23 && wire[15] == 0x45);
    puts("API case4 IPFIX-header PASS");
    assert(memcmp(wire + len - sizeof(expected), expected, sizeof(expected)) == 0);
    puts("API case5 network-byte-order PASS");
    assert(len == 28 && wire[16] == 1 && wire[17] == 1);
    assert(wire[18] == 0 && wire[19] == 12);
    assert(template_len + len <= sizeof(stream));
    memcpy(stream + template_len, wire, len);
    fbSession_t *rs = fbSessionAlloc(model);
    assert(rs != NULL);
    assert(fbSessionAddTemplate(rs, TRUE, 256, template_for(model), &err) == 256);
    fBuf_t *reader = fBufAllocForCollection(rs, NULL);
    assert(reader != NULL);
    assert(fBufSetInternalTemplate(reader, 256, &err));
    /* The reader must learn external 257 from the actual first wire message;
     * only its internal memory template is registered in advance. */
    fBufSetBuffer(reader, stream, template_len + len);
    size_t size = sizeof(out);
    assert(fBufNext(reader, (uint8_t *)out, &size, &err));
    assert(err == NULL && size == sizeof(in));
    assert(memcmp(in, out, sizeof(in)) == 0);
    assert(fbSessionGetDomain(fBufGetSession(reader)) == 0x12345);
    puts("API case6 IPFIX-collection-roundtrip PASS");
    fBufFree(reader);
    fBufFree(writer);
    fbInfoModelFree(model);
    puts("libfixbuf API cases 6/6 PASS");
    return 0;
}
LIBFIXBUF_API_EOF

%build
%configure
%make_build
gcc %{optflags} -UNDEBUG $(pkg-config --cflags glib-2.0) -Iinclude \
    api-smoke.c -Lsrc/.libs -lfixbuf $(pkg-config --libs glib-2.0) -o api-smoke

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -Dpm0755 api-smoke %{buildroot}%{_libexecdir}/libfixbuf-tests/api-smoke
install -Dpm0644 api-smoke.c %{buildroot}%{_libexecdir}/libfixbuf-tests/api-smoke.c

%check
# Unfiltered upstream default check target; this archive defines zero cases.
%make_build check
(cd license-notices; sha256sum -c SHA256SUMS)
LD_LIBRARY_PATH="$PWD/src/.libs" ./api-smoke
# The RPM install-post phase has already stripped the installed helper.
(cd %{buildroot}%{_libexecdir}/libfixbuf-tests; sha256sum api-smoke api-smoke.c > SHA256SUMS)

%files
%license LICENSE.txt license-notices
%doc README NEWS AUTHORS
%{_libdir}/libfixbuf.so*
%{_libdir}/libfixbuf.a
%{_libdir}/pkgconfig/libfixbuf.pc
%dir %{_includedir}/fixbuf
%{_includedir}/fixbuf/*.h
%{_libexecdir}/libfixbuf-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.5.4-1
- Preserve default library configuration and add IPFIX buffer regression checks.
