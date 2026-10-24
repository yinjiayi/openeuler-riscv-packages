# SPDX-License-Identifier: Apache-2.0
Name:           libxdiff
Version:        1.0
Release:        1%{?dist}
Summary:        Standalone text difference and merge library
License:        LGPL-2.1-or-later AND BSD-3-Clause AND FSFULLR AND MIT AND (GPL-2.0-or-later WITH Autoconf-exception-generic) AND (GPL-3.0-or-later WITH Autoconf-exception-generic) AND (GPL-2.0-or-later WITH Libtool-exception) AND ISC
URL:            https://github.com/spotrh/libxdiff
Source0:        libxdiff-1.0.tar.gz
Source1:        gpl-2.0.txt
Source2:        gpl-3.0.txt
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Standalone text difference and three-way merge routines from the spotrh
libxdiff 1.0 Git/libgit2 fork. This is not the incompatible old 0.23 API,
nor a replacement for code bundled inside Git or libgit2.

%prep
%autosetup -n libxdiff-9c6289c5a088bf24f18f0b7bf8acaaf643aa411d -p1
# Keep all 39 exact original members before any helper regeneration. Suffixes
# protect inert copies from recursive configure basename replacement.
mkdir -p license-notices/m4
for notice_file in * m4/*; do
    if test -f "$notice_file"; then
        cp -p "$notice_file" "license-notices/$notice_file.notice"
    fi
done
cp %{SOURCE1} license-notices/GPL-2.0.txt
cp %{SOURCE2} license-notices/GPL-3.0.txt
(
    cd license-notices
    sha256sum *.notice m4/*.notice GPL-2.0.txt GPL-3.0.txt
) > original-notices.sha256
mv original-notices.sha256 license-notices/SHA256SUMS
# Original Automake DIST_COMMON expects README, upstream renamed it .md.
cp -p README.md README
autoreconf -fi

%build
%configure
%make_build
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
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <xdiff.h>

struct output { char text[4096]; size_t size; };
static int emit(void *data, mmbuffer_t *buf, int count)
{
    struct output *out = data;
    int i;
    for (i = 0; i < count; i++) {
        assert(buf[i].size < sizeof out->text - out->size);
        memcpy(out->text + out->size, buf[i].ptr, buf[i].size);
        out->size += buf[i].size;
    }
    out->text[out->size] = 0;
    return 0;
}
static void diff_case(char *left, char *right, unsigned long flags, int changed)
{
    mmfile_t a = {left, strlen(left)}, b = {right, strlen(right)};
    xpparam_t param = {flags};
    xdemitconf_t conf;
    struct output out;
    xdemitcb_t cb = {&out, emit};
    long size = 0;
    memset(&out, 0, sizeof out);
    memset(&conf, 0, sizeof conf);
    assert(xdl_mmfile_size(&a) == (long)strlen(left));
    assert(xdl_mmfile_first(&a, &size) == left && size == (long)strlen(left));
    assert(xdl_diff(&a, &b, &param, &conf, &cb) == 0);
    if (changed) {
        assert(strstr(out.text, "-old\n") != NULL);
        assert(strstr(out.text, "+new\n") != NULL);
    } else {
        assert(out.size == 0);
    }
}
int main(void)
{
    mmfile_t base = {"base\n", 5}, ours = {"ours\n", 5}, theirs = {"base\n", 5};
    xmparam_t param;
    mmbuffer_t merged;
    diff_case("same\n", "same\n", 0, 0);
    /* Long lines and a non-eight-byte line offset exercise default fast hash. */
    diff_case("prefix-1234567890\nold\nsuffix-1234567890\n",
              "prefix-1234567890\nnew\nsuffix-1234567890\n", XDF_NEED_MINIMAL, 1);
    diff_case("prefix-1234567890\nold\nsuffix-1234567890\n",
              "prefix-1234567890\nnew\nsuffix-1234567890\n", XDF_PATIENCE_DIFF, 1);
    diff_case("prefix-1234567890\nold\nsuffix-1234567890\n",
              "prefix-1234567890\nnew\nsuffix-1234567890\n", XDF_HISTOGRAM_DIFF, 1);
    diff_case("a b\n", "a  b\n", XDF_IGNORE_WHITESPACE, 0);
    memset(&param, 0, sizeof param);
    param.level = XDL_MERGE_ZEALOUS;
    assert(xdl_merge(&base, &ours, &theirs, &param, &merged) == 0);
    assert(merged.size == 5 && memcmp(merged.ptr, "ours\n", 5) == 0);
    free(merged.ptr);
    puts("libxdiff api-smoke: 6 cases passed; version 1.0");
    return 0;
}
EOF
cp api-smoke.c license-notices/api-smoke.c
gcc %{optflags} -UNDEBUG -I. api-smoke.c -L.libs -lxdiff \
    %{?build_ldflags} -o api-smoke

%install
%make_install
rm -f %{buildroot}%{_libdir}/libxdiff.la
install -Dm755 api-smoke %{buildroot}%{_libexecdir}/libxdiff-tests/api-smoke

%check
set -eu
export LC_ALL=C
(
    cd license-notices
    sha256sum -c SHA256SUMS
)
# Original check-am: all-am contains no TESTS/check_PROGRAMS.
%make_build check
LD_LIBRARY_PATH="$PWD/.libs" ./api-smoke
(
    cd %{buildroot}%{_libexecdir}/libxdiff-tests
    sha256sum api-smoke > SHA256SUMS
)

%files
%license COPYING AUTHORS license-notices
%doc README.md NEWS ChangeLog
%{_libdir}/libxdiff.so
%{_libdir}/libxdiff.so.1
%{_libdir}/libxdiff.so.1.0.0
%{_libdir}/libxdiff.a
%{_libdir}/pkgconfig/libxdiff.pc
%{_includedir}/xdiff
%{_libexecdir}/libxdiff-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0-1
- Preserve upstream defaults and zero-case check; add installed API checks.
