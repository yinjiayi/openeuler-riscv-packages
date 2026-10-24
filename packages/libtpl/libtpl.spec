# SPDX-License-Identifier: Apache-2.0
Name:           libtpl
Version:        1.6.1
Release:        1%{?dist}
Summary:        Lightweight C serialization library
License:        BSD-1-Clause AND GPL-2.0-or-later AND ISC
URL:            https://troydhanson.github.io/tpl/
Source0:        tpl-1.6.1.tar.gz
Source1:        gpl-2.0.txt
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Serialization of C scalars, fixed and dynamic arrays, and binary buffers.
Default shared and static libraries and the original self-test suite are
preserved, with an additional deterministic userspace API regression driver.

%prep
%autosetup -n tpl-5ac54fe7beab67cbfb6f95552c15a68204a014bd -p1
# Preserve all 399 fixed-source members before autoreconf/configure changes
# active helpers; inert suffixes avoid RPM macro recursive helper replacement.
find . -path ./license-notices -prune -o -type f -print | while IFS= read -r original; do
    mkdir -p "license-notices/$(dirname "$original")"
    cp -p "$original" "license-notices/$original.notice"
done
cp -p %{SOURCE1} license-notices/GPL-2.0.txt
(cd license-notices; find . -type f -print | LC_ALL=C sort | xargs sha256sum) > original-notices.sha256
mv original-notices.sha256 license-notices/SHA256SUMS
find license-notices -type f -exec chmod 0644 {} +
test "$(find license-notices -type f | wc -l)" -eq 401
cat > api-smoke.c <<'LIBTPL_API_EOF'
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
#include <tpl.h>
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static void *image(tpl_node *writer, size_t *size) {
    void *data = NULL;
    assert(writer != NULL);
    assert(tpl_dump(writer, TPL_MEM, &data, size) == 0);
    assert(data != NULL && *size > 8);
    tpl_free(writer);
    return data;
}
static void load(tpl_node *reader, void *data, size_t size) {
    assert(reader != NULL);
    assert(tpl_load(reader, TPL_MEM, data, size) == 0);
}
int main(void) {
    size_t size = 0;
    void *data;
    tpl_node *n;
    setvbuf(stdout, NULL, _IONBF, 0);
    int in = -1234567, out = 0;
    n = tpl_map("i", &in); assert(n != NULL);
    assert(tpl_pack(n, 0) == 0); data = image(n, &size);
    n = tpl_map("i", &out); load(n, data, size);
    assert(tpl_unpack(n, 0) == 1 && out == in);
    tpl_free(n); free(data);
    puts("API case1 signed-integer PASS");

    int16_t sin = -32767, sout = 0;
    uint16_t uin = 65535, uout = 0;
    n = tpl_map("jv", &sin, &uin); assert(n != NULL);
    assert(tpl_pack(n, 0) == 0); data = image(n, &size);
    n = tpl_map("jv", &sout, &uout); load(n, data, size);
    assert(tpl_unpack(n, 0) == 1 && sout == sin && uout == uin);
    tpl_free(n); free(data);
    puts("API case2 narrow-integers PASS");

    double din = -1234.5, dout = 0.0;
    n = tpl_map("f", &din); assert(n != NULL);
    assert(tpl_pack(n, 0) == 0); data = image(n, &size);
    n = tpl_map("f", &dout); load(n, data, size);
    assert(tpl_unpack(n, 0) == 1 && dout == din);
    tpl_free(n); free(data);
    puts("API case3 double PASS");

    int fixed_in[5] = {0, -1, 2, -300, 40000}, fixed_out[5] = {0};
    n = tpl_map("i#", fixed_in, 5); assert(n != NULL);
    assert(tpl_pack(n, 0) == 0); data = image(n, &size);
    n = tpl_map("i#", fixed_out, 5); load(n, data, size);
    assert(tpl_unpack(n, 0) == 1);
    assert(memcmp(fixed_in, fixed_out, sizeof(fixed_in)) == 0);
    tpl_free(n); free(data);
    puts("API case4 fixed-array PASS");

    unsigned char bytes[] = {0, 1, 127, 128, 255, 0, 42};
    tpl_bin bin_in = {bytes, sizeof(bytes)}, bin_out = {NULL, 0};
    n = tpl_map("B", &bin_in); assert(n != NULL);
    assert(tpl_pack(n, 0) == 0); data = image(n, &size);
    n = tpl_map("B", &bin_out); load(n, data, size);
    assert(tpl_unpack(n, 0) == 1 && bin_out.sz == sizeof(bytes));
    assert(bin_out.addr != NULL && memcmp(bin_out.addr, bytes, sizeof(bytes)) == 0);
    tpl_free(n); free(data); free(bin_out.addr);
    puts("API case5 binary-buffer PASS");

    int item = 0, received = 0;
    n = tpl_map("A(i)", &item); assert(n != NULL);
    for (item = 1; item <= 7; ++item) assert(tpl_pack(n, 1) == 0);
    data = image(n, &size);
    n = tpl_map("A(i)", &received); load(n, data, size);
    assert(tpl_Alen(n, 1) == 7);
    for (int expected = 1; expected <= 7; ++expected) {
        assert(tpl_unpack(n, 1) == 8 - expected && received == expected);
    }
    assert(tpl_Alen(n, 1) == 0 && tpl_unpack(n, 1) == 0);
    tpl_free(n); free(data);
    puts("API case6 dynamic-array PASS");
    puts("libtpl API cases 6/6 PASS");
    return 0;
}
LIBTPL_API_EOF

%build
autoreconf -fiv
%configure
%make_build
gcc %{optflags} -UNDEBUG -Isrc api-smoke.c -Lsrc/.libs -ltpl -o api-smoke

%install
%make_install
find %{buildroot} -name '*.la' -delete
install -Dpm0755 api-smoke %{buildroot}%{_libexecdir}/libtpl-tests/api-smoke
install -Dpm0644 api-smoke.c %{buildroot}%{_libexecdir}/libtpl-tests/api-smoke.c

%check
# Retain automake check and the README's original Linux default self-test.
%make_build check
# Serial invocation avoids original run_tests target racing its program build.
# Original runner compares 124 answer files; all 125 programs are compiled.
make -C tests -j1
test -x tests/test125
(cd license-notices; sha256sum -c SHA256SUMS)
LD_LIBRARY_PATH="$PWD/src/.libs" ./api-smoke
# install-post stripping precedes check; bind the actual packaged helper bytes.
(cd %{buildroot}%{_libexecdir}/libtpl-tests; sha256sum api-smoke api-smoke.c > SHA256SUMS)

%files
%license LICENSE license-notices
%doc README README.md doc
%{_libdir}/libtpl.so*
%{_libdir}/libtpl.a
%{_includedir}/tpl.h
%{_libexecdir}/libtpl-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.1-1
- Preserve default libraries, original suite, and complete embedded notices.
- Add serialization roundtrips and installed shared-library binding checks.
