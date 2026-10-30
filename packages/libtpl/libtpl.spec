# SPDX-License-Identifier: Apache-2.0
Name:           libtpl
Version:        1.6.1
Release:        1%{?dist}
Summary:        Lightweight C serialization library
License:        BSD-1-Clause AND GPL-2.0-or-later AND ISC
URL:            https://troydhanson.github.io/tpl/
Source0:        tpl-1.6.1.tar.gz
Source1:        gpl-2.0.txt
Patch0:         0001-free-output-buffer-after-fd-rollback.patch
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
BuildRequires:  patch
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Serialization of C scalars, fixed and dynamic arrays, and binary buffers.
Default shared and static libraries and the original self-test suite are
preserved, with an additional deterministic userspace API regression driver.

%prep
%setup -q -n tpl-5ac54fe7beab67cbfb6f95552c15a68204a014bd
# Preserve all 399 fixed-source members before autopatch/autoreconf/configure changes
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
echo '0a17be1d7fc9521f4622346f606213d7358672f61c56334c8f8cf1e551ba71bd  license-notices/src/tpl.c.notice' | sha256sum -c -
%autopatch -p1
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
cat > fd-rollback-regression.c <<'LIBTPL_FD_EOF'
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
 *
 * Target-CI-only regression. Local tooling validation does not compile or run it.
 * Link with the actual static tpl object and GNU ld --wrap for the four
 * external calls below; do not preload wrappers into installed shared QA.
 */
#define _POSIX_C_SOURCE 200809L
#include <tpl.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

extern ssize_t __real_write(int, const void *, size_t);
extern int __real_fstat(int, struct stat *);
extern int __real_ftruncate(int, off_t);
extern void __real_free(void *);

static int armed, watched_fd = -1, phase, release_count;
static const unsigned char *watched;
static size_t requested;
static off_t original_size;
static char events[8];
static size_t event_count;
static const char prefix[] = "libtpl rollback prefix\n";

static void fail(const char *expression, int line) {
    fprintf(stderr, "FAULT regression check failed line=%%d: %%s\n", line, expression);
    _Exit(98);
}
#define CHECK(x) do { if (!(x)) fail(#x, __LINE__); } while (0)
static void event(char c) {
    CHECK(event_count + 1 < sizeof events);
    events[event_count++] = c;
    events[event_count] = '\0';
}

ssize_t __wrap_write(int fd, const void *buffer, size_t count) {
    if (!armed || fd != watched_fd) return __real_write(fd, buffer, count);
    CHECK(release_count == 0);
    if (phase == 0) {
        CHECK(count > 3 && memcmp(buffer, "tpl", 3) == 0);
        watched = buffer;
        requested = count;
        CHECK(__real_write(fd, buffer, 3) == 3);
        event('P');
        phase = 1;
        return 3;                       /* actual partial write, not just a stub */
    }
    CHECK(phase == 1 && buffer == watched + 3 && count == requested - 3);
    event('E');
    phase = 2;
    errno = EIO;                        /* neither retryable EINTR nor EAGAIN */
    return -1;
}

int __wrap_fstat(int fd, struct stat *result) {
    if (!armed || fd != watched_fd) return __real_fstat(fd, result);
    CHECK(phase == 2 && release_count == 0 && watched != NULL);
    CHECK(__real_fstat(fd, result) == 0);
    CHECK(S_ISREG(result->st_mode) && result->st_size == original_size + 3);
    event('S');
    phase = 3;
    return 0;
}

int __wrap_ftruncate(int fd, off_t length) {
    if (!armed || fd != watched_fd) return __real_ftruncate(fd, length);
    CHECK(phase == 3 && release_count == 0 && watched != NULL);
    CHECK(length == original_size);
    CHECK(__real_ftruncate(fd, length) == 0);
    event('T');
    phase = 4;
    return 0;
}

void __wrap_free(void *pointer) {
    if (armed && watched != NULL && pointer == watched) {
        if (phase != 4) {
            fputs("FAULT order violation: free before rollback\n", stderr);
            _Exit(97);                  /* exact negative-control signature */
        }
        CHECK(release_count == 0);
        event('F');
        watched = NULL;                 /* never compare a freed pointer later */
        release_count++;
        __real_free(pointer);
        phase = 5;
        return;
    }
    __real_free(pointer);
}

int main(void) {
    char filename[] = "libtpl-fd-rollback-XXXXXX";
    char actual[sizeof prefix] = {0};
    struct stat result;
    int value = 1234567;
    tpl_node *node;
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    original_size = (off_t)(sizeof prefix - 1);
    watched_fd = mkstemp(filename);
    CHECK(watched_fd >= 0);
    CHECK(unlink(filename) == 0);        /* no retained file even if process fails */
    CHECK(__real_write(watched_fd, prefix, sizeof prefix - 1) == original_size);
    node = tpl_map("i", &value);
    CHECK(node != NULL && tpl_pack(node, 0) == 0);
    armed = 1;
    CHECK(tpl_dump(node, TPL_FD, watched_fd) == -1);
    armed = 0;
    CHECK(phase == 5 && release_count == 1 && watched == NULL);
    CHECK(event_count == 5 && strcmp(events, "PESTF") == 0);
    CHECK(__real_fstat(watched_fd, &result) == 0 && result.st_size == original_size);
    CHECK(pread(watched_fd, actual, sizeof prefix - 1, 0) == original_size);
    CHECK(memcmp(actual, prefix, sizeof prefix - 1) == 0);
    CHECK(close(watched_fd) == 0);
    tpl_free(node);
    puts("libtpl TPL_FD rollback regression PASS sequence=PESTF status=-1 bytes=3 frees=1");
    return 0;
}
LIBTPL_FD_EOF

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
# Target-only exact fatal-write lifetime regression, separate from original QA.
# Build both from real objects: patched default static archive and preserved original C.
export LC_ALL=C
mkdir fd-rollback-results
nm -u src/.libs/libtpl.a > fd-rollback-results/patched-static-undefined-symbols.txt
for symbol in write fstat ftruncate free; do
    grep -Eq "[[:space:]]U[[:space:]]+$symbol$" fd-rollback-results/patched-static-undefined-symbols.txt
done
set -x
gcc %{optflags} -UNDEBUG -Isrc fd-rollback-regression.c src/.libs/libtpl.a \
    -Wl,--wrap=write -Wl,--wrap=fstat -Wl,--wrap=ftruncate -Wl,--wrap=free \
    -o fd-rollback-results/patched-regression
gcc %{optflags} -UNDEBUG -Isrc fd-rollback-regression.c \
    -x c license-notices/src/tpl.c.notice -x none \
    -Wl,--wrap=write -Wl,--wrap=fstat -Wl,--wrap=ftruncate -Wl,--wrap=free \
    -o fd-rollback-results/original-negative-control
set +x
sha256sum fd-rollback-regression.c license-notices/src/tpl.c.notice \
    src/tpl.c src/.libs/libtpl.a fd-rollback-results/*
if fd-rollback-results/original-negative-control > fd-rollback-results/original.stdout 2> fd-rollback-results/original.stderr; then
    original_status=0
else
    original_status=$?
fi
printf '%%s\n' "$original_status" > fd-rollback-results/original.exit
cat fd-rollback-results/original.stdout fd-rollback-results/original.stderr
sha256sum fd-rollback-results/original.*
test "$original_status" -eq 97
test ! -s fd-rollback-results/original.stdout
test "$(grep -Fxc 'FAULT order violation: free before rollback' fd-rollback-results/original.stderr)" -eq 1
test "$(wc -l < fd-rollback-results/original.stderr)" -eq 2
grep -Ex 'error writing to fd [0-9]+: Input/output error' fd-rollback-results/original.stderr
if fd-rollback-results/patched-regression > fd-rollback-results/patched.stdout 2> fd-rollback-results/patched.stderr; then
    patched_status=0
else
    patched_status=$?
fi
printf '%%s\n' "$patched_status" > fd-rollback-results/patched.exit
cat fd-rollback-results/patched.stdout fd-rollback-results/patched.stderr
sha256sum fd-rollback-results/patched.*
test "$patched_status" -eq 0
test "$(wc -l < fd-rollback-results/patched.stdout)" -eq 1
grep -Fx 'libtpl TPL_FD rollback regression PASS sequence=PESTF status=-1 bytes=3 frees=1' fd-rollback-results/patched.stdout
test "$(wc -l < fd-rollback-results/patched.stderr)" -eq 1
grep -Ex 'error writing to fd [0-9]+: Input/output error' fd-rollback-results/patched.stderr
echo 'libtpl exact original-negative exit=97 and patched-positive exit=0 PASS'
# install-post stripping precedes check; bind the actual packaged helper bytes.
(cd %{buildroot}%{_libexecdir}/libtpl-tests; sha256sum api-smoke api-smoke.c > SHA256SUMS)

%files
%license LICENSE license-notices
%doc README README.md doc fd-rollback-regression.c
%{_libdir}/libtpl.so*
%{_libdir}/libtpl.a
%{_includedir}/tpl.h
%{_libexecdir}/libtpl-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.1-1
- Preserve default libraries, original suite, and complete embedded notices.
- Add serialization roundtrips and installed shared-library binding checks.
- Retain the dump buffer through fatal-write rollback with exact target controls.
