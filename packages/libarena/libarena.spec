# SPDX-License-Identifier: MIT
Name:           libarena
Version:        0.3.7
Release:        1%{?dist}
Summary:        Custom memory allocator interface for C
License:        MIT AND BSD-3-Clause AND LicenseRef-dh-make-output
URL:            https://25thandclement.com/~william/projects/libarena.html
Source0:        https://25thandclement.com/~william/projects/releases/libarena-%{version}.tgz
Patch0:         0001-pass-ldflags-to-shared-link.patch
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  patch
BuildRequires:  sed
BuildRequires:  tar
BuildRequires:  zlib-devel
Requires:       bash
Requires:       binutils
Requires:       coreutils
Requires:       diffutils
Requires:       gawk
Requires:       grep

%description
Libarena provides stack-like arena and pooled allocators behind a common C
interface. Original static construction, optional shared target and original
randomized CRC regression are retained. Added fixed-input API cases are not
allocator security, stress, timing or performance certification.

%prep
%setup -q
# Snapshot all33 original ordinary members BEFORE applying even our link fix.
mkdir source-notices
for path in GNUmakefile Makefile.mingw Makefile.osx Rules.mk debian/* mk/* regress/* src/*; do
    test -f "$path"
    mkdir -p "source-notices/$(dirname "$path")"
    cp -p "$path" "source-notices/$path.notice"
done
(cd source-notices; sha256sum *.notice debian/*.notice mk/*.notice regress/*.notice src/*.notice) > source-notices.sha256
test "$(wc -l < source-notices.sha256)" -eq 33
mv source-notices.sha256 source-notices/SHA256SUMS
# Preserve the complete exact output exception, not an inferred GPL/MIT grant.
sed -n '1,7p' debian/rules > LicenseRef-dh-make-output.txt
%autopatch -p1
cat > api-smoke.c <<'LIBARENA_API_EOF'
/*
 * Copyright (c) 2026 yinjiayi
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
#include <stddef.h>
#include <stdint.h>
#include <stdarg.h>
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <arena/proto.h>
#include <arena/pool.h>

/* Volatile calls retain six real dynamic relocations for installed QA. */
static ARENA *(*volatile aopen)(const struct arena_options *, const struct arena_prototype *) = arena_open;
static void *(*volatile amalloc)(ARENA *, size_t, size_t) = arena_malloc;
static void *(*volatile arealloc)(ARENA *, void *, size_t, size_t) = arena_realloc;
static POOL *(*volatile popen_)(const struct pool_options *, const struct arena_prototype *) = pool_open;
static void *(*volatile pget)(POOL *, size_t, size_t) = pool_get;
static void *(*volatile prealloc)(POOL *, void *, size_t, size_t) = pool_realloc;

static void pattern(unsigned char *p, size_t n) {
    for (size_t i = 0; i < n; ++i) p[i] = (unsigned char)(i * 17u + 3u);
}
static void preserved(const unsigned char *p, size_t n) {
    for (size_t i = 0; i < n; ++i) assert(p[i] == (unsigned char)(i * 17u + 3u));
}
int main(void) {
    ARENA *a = aopen(NULL, NULL);
    assert(a);
    unsigned char *x = amalloc(a, 64, 32);
    assert(x && (uintptr_t)x % 32 == 0);
    pattern(x, 64);
    x = arealloc(a, x, 512, 64);
    assert(x && (uintptr_t)x % 64 == 0);
    preserved(x, 64);
    arena_free(a, x);
    arena_close(a);
    puts("case 1 arena-aligned-reallocation PASS");

    a = aopen(NULL, NULL);
    assert(a);
    void *mark = NULL;
    arena_mark(a, &mark);
    x = amalloc(a, 47, 16);
    assert(x);
    pattern(x, 47);
    arena_reset(a, mark);
    unsigned char *again = amalloc(a, 47, 16);
    assert(again == x);
    arena_close(a);
    puts("case 2 arena-mark-reset PASS");

    POOL *p = popen_(NULL, NULL);
    assert(p);
    x = pget(p, 37, 16);
    assert(x && (uintptr_t)x % 16 == 0);
    pattern(x, 37);
    x = prealloc(p, x, 1024, 64);
    assert(x && (uintptr_t)x % 64 == 0);
    preserved(x, 37);
    pool_put(p, x);
    pool_close(p);
    puts("case 3 pool-bucket-reallocation PASS");

    a = aopen(NULL, NULL);
    assert(a);
    const struct arena_prototype *parent = arena_export(a);
    assert(parent && arena_import(parent) == a);
    p = popen_(NULL, parent);
    assert(p && pool_import(pool_export(p)) == p);
    x = pget(p, 93, 32);
    assert(x && (uintptr_t)x % 32 == 0);
    pattern(x, 93);
    preserved(x, 93);
    pool_put(p, x);
    pool_close(p);
    arena_close(a);
    puts("case 4 layered-prototype-ownership PASS");

    a = aopen(NULL, NULL);
    assert(a);
    char *s = arena_strdup(a, "allocator-roundtrip");
    char *short_s = arena_strndup(a, "abcdef", 3);
    const unsigned char binary[] = {0, 1, 0xff, 0, 7};
    unsigned char *copy = arena_memdup(a, binary, sizeof binary);
    char *formatted = NULL;
    assert(s && !strcmp(s, "allocator-roundtrip"));
    assert(short_s && !strcmp(short_s, "abc"));
    assert(copy && !memcmp(copy, binary, sizeof binary));
    assert(arena_asprintf(a, &formatted, "%s:%u", "arena", 37u) == 8);
    assert(formatted && !strcmp(formatted, "arena:37"));
    arena_close(a);
    puts("case 5 exact-string-binary-format PASS");

    a = aopen(NULL, NULL);
    assert(a && amalloc(a, 0, 0) == NULL);
    x = arealloc(a, NULL, 23, 16);
    assert(x);
    pattern(x, 23);
    assert(arealloc(a, x, 0, 0) == NULL);
    arena_close(a);
    p = popen_(NULL, NULL);
    assert(p);
    x = prealloc(p, NULL, 29, 16);
    assert(x);
    assert(prealloc(p, x, 0, 0) == NULL);
    pool_close(p);
    puts("case 6 zero-size-reallocation PASS");
    puts("libarena API 6/6 PASS");
    return 0;
}
LIBARENA_API_EOF

%build
# First run unmodified original default static target, then ORIGINAL optional pic.
%make_build all CC=gcc CFLAGS='%{optflags}' CPPFLAGS='-I%{_includedir}' LDFLAGS='%{build_ldflags}' prefix=%{_prefix} libdir=%{_libdir}
%make_build pic CC=gcc CFLAGS='%{optflags}' CPPFLAGS='-I%{_includedir}' LDFLAGS='%{build_ldflags}' prefix=%{_prefix} libdir=%{_libdir}

%install
make install DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir}
install -d %{buildroot}%{_libexecdir}/libarena %{buildroot}%{_datadir}/libarena-tests
gcc %{optflags} -UNDEBUG -Wall -Wextra -Werror -I%{buildroot}%{_includedir} api-smoke.c \
    -L%{buildroot}%{_libdir} -Wl,--no-as-needed -larena %{build_ldflags} \
    -o %{buildroot}%{_libexecdir}/libarena/api-smoke
install -m 0644 api-smoke.c %{buildroot}%{_datadir}/libarena-tests/api-smoke.c

%check
# Original check builds stacked+grow, executes stacked only: never omit/reseed it.
make check CC=gcc CFLAGS='%{optflags}' CPPFLAGS='-I%{_includedir}' LDFLAGS='%{build_ldflags}' prefix=%{_prefix} libdir=%{_libdir}
env LD_LIBRARY_PATH=%{buildroot}%{_libdir} %{buildroot}%{_libexecdir}/libarena/api-smoke
(cd source-notices; sha256sum -c SHA256SUMS)
# RPM install-post has already stripped installed ELF at this lifecycle point.
(cd %{buildroot}; sha256sum .%{_libexecdir}/libarena/api-smoke .%{_datadir}/libarena-tests/api-smoke.c) > %{buildroot}%{_datadir}/libarena-tests/SHA256SUMS

%files
%license source-notices LicenseRef-dh-make-output.txt
%{_libdir}/libarena.a
%{_libdir}/libarena.la
%{_libdir}/libarena.so
%{_libdir}/libarena.so.0
%{_libdir}/libarena.so.0.0.3
%dir %{_includedir}/arena
%{_includedir}/arena/arena.h
%{_includedir}/arena/pool.h
%{_includedir}/arena/proto.h
%{_includedir}/arena/rbits.h
%{_includedir}/arena/util.h
%{_includedir}/arena/align.h
%dir %{_libexecdir}/libarena
%{_libexecdir}/libarena/api-smoke
%dir %{_datadir}/libarena-tests
%{_datadir}/libarena-tests/api-smoke.c
%{_datadir}/libarena-tests/SHA256SUMS

%changelog
* Sun Oct 25 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.3.7-1
- Preserve original static/default regression; add shared-link hardening and strict API QA.
