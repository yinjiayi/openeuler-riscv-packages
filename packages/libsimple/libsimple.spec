# SPDX-License-Identifier: MIT
Name:           libsimple
Version:        1.8
Release:        1%{?dist}
Summary:        General-purpose C utility functions
License:        ISC
URL:            https://codeberg.org/maandree/libsimple
Source0:        libsimple-1.8.tar.gz
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  sed
BuildRequires:  tar
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
libsimple provides general-purpose C allocation, string, memory, numeric,
time-conversion and other utility functions. Both upstream static and shared
libraries, public headers and complete committed manuals are included.

%prep
%autosetup -n libsimple -p1
set -eu
set -o pipefail
# Preserve all original ordinary source members before adding the API driver.
mkdir license-notices
find . -path ./license-notices -prune -o -type f -print0 | sort -z |
while IFS= read -r -d '' source; do
    relative=${source#./}
    mkdir -p "license-notices/$(dirname "$relative")"
    cp -- "$source" "license-notices/$relative.notice"
done
test "$(find license-notices -type f | wc -l)" -eq 1353
(cd license-notices && find . -type f -print0 | sort -z | xargs -0 sha256sum) > original-notice-sha256
mv original-notice-sha256 license-notices/SHA256SUMS

cat > api-smoke.c <<'LIBSIMPLE_API_EOF'
/* SPDX-License-Identifier: ISC
 * Copyright (c) 2026 openEuler RISC-V Maintainers
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 * Package-local functional checks, not upstream tests or native timing claims.
 */
#include <libsimple.h>
#include <assert.h>

char *argv0;
static void *(*volatile call_memdup)(const void *, size_t) = libsimple_memdup;
static int (*volatile call_strtoi)(const char *restrict, char **restrict, int) = libsimple_strtoi;
static int (*volatile call_strstarts)(const char *, const char *) = libsimple_strstarts;
static int (*volatile call_memcasecmp)(const void *, const void *, size_t) = libsimple_memcasecmp;
static void *(*volatile call_memmem)(const void *, size_t, const void *, size_t) = libsimple_memmem;
static int (*volatile call_strtotimespec)(struct timespec *restrict, const char *restrict, char **restrict) = libsimple_strtotimespec;

int main(int argc, char **argv)
{
    const unsigned char binary[] = {0x00, 0xff, 0x23, 0xa5};
    const unsigned char hay[] = {0, 1, 2, 0, 3, 4, 0, 3, 4};
    const unsigned char needle[] = {0, 3, 4};
    const unsigned char absent[] = {0, 9};
    const char mixed_a[] = {'A', 0, 'z'};
    const char mixed_b[] = {'a', 0, 'Z'};
    const char invalid[] = "x";
    unsigned char *copy;
    struct timespec ts;
    char *end;
    (void)argc;
    argv0 = argv[0];

    copy = call_memdup(binary, sizeof(binary));
    assert(copy && copy != binary && !memcmp(copy, binary, sizeof(binary)));
    copy[1] = 7;
    assert(binary[1] == 0xff);
    free(copy);
    puts("API 1/6: binary allocation and independent ownership");

    errno = 0;
    assert(call_strtoi("0x7f tail", &end, 0) == 127 && !errno && !strcmp(end, " tail"));
    errno = 0;
    assert(call_strtoi("99999999999999999999999999999999999", &end, 10) == INT_MAX);
    assert(errno == ERANGE && !*end);
    puts("API 2/6: integer parsing, end pointer and overflow");

    assert(call_strstarts("prefix-and-body", "prefix-") == 1);
    assert(call_strstarts("prefix-and-body", "Prefix-") == 0);
    assert(call_strstarts("", "") == 1);
    puts("API 3/6: exact prefix semantics");

    assert(call_memcasecmp(mixed_a, mixed_b, sizeof(mixed_a)) == 0);
    assert(call_memcasecmp("abc", "AbD", 3) < 0);
    assert(call_memcasecmp("abc", "ZZZ", 0) == 0);
    puts("API 4/6: bounded case comparison including embedded NUL");

    assert(call_memmem(hay, sizeof(hay), needle, sizeof(needle)) == hay + 3);
    assert(call_memmem(hay, sizeof(hay), needle, 0) == hay);
    assert(call_memmem(hay, sizeof(hay), absent, sizeof(absent)) == NULL);
    puts("API 5/6: binary subsequence, empty and absent matches");

    errno = 0;
    assert(call_strtotimespec(&ts, "1.25tail", &end) == 0 && !errno);
    assert(ts.tv_sec == 1 && ts.tv_nsec == 250000000L && !strcmp(end, "tail"));
    assert(call_strtotimespec(&ts, "-0.125!", &end) == 0);
    assert(ts.tv_sec == -1 && ts.tv_nsec == 875000000L && !strcmp(end, "!"));
    errno = 0;
    assert(call_strtotimespec(&ts, invalid, &end) == -1 && errno == EINVAL && end == invalid);
    puts("API 6/6: decimal timespec conversion and strict error path");
    puts("libsimple additional API cases: 6/6");
    return 0;
}
LIBSIMPLE_API_EOF

%build
set -eu
# Preserve upstream C11, feature macros, warnings and libm; RPM handles stripping.
%make_build CC="%{__cc} -std=c11" CFLAGS="%{optflags} -Wall -Wextra -UNDEBUG" CPPFLAGS="-D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -lm"
%{__cc} -std=c11 %{optflags} -UNDEBUG -D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE -I. api-smoke.c -L. -lsimple -lm %{build_ldflags} -o api-smoke

%install
set -eu
%make_install PREFIX=%{_prefix} MANPREFIX=%{_mandir}
# Upstream has no LIBDIR variable: move the entire normal four-entry library set.
mkdir -p %{buildroot}%{_libdir}
for library in libsimple.a libsimple.so libsimple.so.1 libsimple.so.1.8; do
    test -e "%{buildroot}%{_prefix}/lib/$library"
    mv -- "%{buildroot}%{_prefix}/lib/$library" "%{buildroot}%{_libdir}/$library"
done
test "$(find %{buildroot}%{_includedir}/libsimple -type f | wc -l)" -eq 48
test -f %{buildroot}%{_includedir}/libsimple.h
test -f %{buildroot}%{_includedir}/libsimple-arg.h
test "$(find %{buildroot}%{_mandir}/man0 %{buildroot}%{_mandir}/man3 \( -type f -o -type l \) | wc -l)" -eq 842
install -d %{buildroot}%{_libexecdir}/libsimple-tests
install -m 0755 api-smoke %{buildroot}%{_libexecdir}/libsimple-tests/api-smoke
install -m 0644 api-smoke.c %{buildroot}%{_libexecdir}/libsimple-tests/api-smoke.c

%check
set -eu
set -o pipefail
# Keep all 1074 original programs and the original fail-fast check loop unchanged.
if make check CC="%{__cc} -std=c11" CFLAGS="%{optflags} -Wall -Wextra -UNDEBUG" CPPFLAGS="-D_DEFAULT_SOURCE -D_BSD_SOURCE -D_XOPEN_SOURCE=700 -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -lm" > upstream-check.log 2>&1; then
    cat upstream-check.log
else
    status=$?
    cat upstream-check.log >&2
    exit "$status"
fi
test "$(grep -Ec '^\./[^/[:space:]]+\.test$' upstream-check.log)" -eq 1074
if grep -E -e 'Some tests have not been ran' -e 'warning: libsimple_[A-Za-z0-9_]+ missing' upstream-check.log; then
    echo 'Upstream reports unexecuted conditional test branches' >&2
    exit 1
fi
echo 'libsimple original check invocations: 1074/1074 (includes upstream no-op programs)'
(cd license-notices && test "$(wc -l < SHA256SUMS)" -eq 1353 && sha256sum -c SHA256SUMS)
LD_LIBRARY_PATH="$PWD" ./api-smoke
# install-post (including RPM stripping) precedes check: bind final payload bytes.
(cd %{buildroot}%{_libexecdir}/libsimple-tests && sha256sum api-smoke api-smoke.c > SHA256SUMS)

%files
%license LICENSE license-notices
%doc README
%{_libdir}/libsimple.so.1.8
%{_libdir}/libsimple.so.1
%{_libdir}/libsimple.so
%{_libdir}/libsimple.a
%{_includedir}/libsimple.h
%{_includedir}/libsimple-arg.h
%{_includedir}/libsimple/
%{_mandir}/man0/libsimple*.0*
%{_mandir}/man3/libsimple_*.3.*
%{_mandir}/man3/LIBSIMPLE_*.3.*
%{_mandir}/man3/*.3libsimple*
%{_libexecdir}/libsimple-tests/

%changelog
* Sun Oct 25 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.8-1
- Preserve default libraries, headers, manuals and every original check program.
- Add binary/numeric utility API checks and strict installed-library bindings.
