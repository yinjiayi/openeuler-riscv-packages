# SPDX-License-Identifier: Apache-2.0
Name:           libgcroots
Version:        0.3.2
Release:        1%{?dist}
Summary:        Non-threaded garbage collector root acquisition library
# Binary library/header: Boehm-GC. Source-only m4 notices and full GPL3 retained.
License:        Boehm-GC
URL:            https://github.com/uim/libgcroots
Source0:        https://codeload.github.com/uim/libgcroots/tar.gz/d362356cc4c5f591695d2fbda7746918250c9e99#/libgcroots-0.3.2.tar.gz
Source1:        https://www.gnu.org/licenses/gpl-3.0.txt#/COPYING.GPL3
BuildRequires:  gcc glibc-devel make autoconf automake libtool pkgconf gzip
BuildRequires:  coreutils findutils grep sed binutils

%description
Architecture-dependent root acquisition, not a complete garbage collector.
Only the original non-threaded protected-call contexts are supported.

%package devel
Summary:        Public header, link libraries and downstream contract tests
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc glibc-devel pkgconf coreutils binutils grep

%description devel
Unmodified public header, pkg-config metadata, shared/static linking files and
separately identified downstream lifecycle and stack-snapshot contract tests.

%prep
%setup -q -n libgcroots-d362356cc4c5f591695d2fbda7746918250c9e99
cp %{SOURCE1} COPYING.GPL3
autoreconf --force --install --verbose
cat > gcroots-contract.c <<'C'
/* SPDX-License-Identifier: Apache-2.0
 * Original downstream fixture, not an upstream unit suite or full GC test.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gcroots.h>
#if !defined(__riscv) || __riscv_xlen != 64
#error This downstream fixture requires the declared riscv64 target
#endif
#ifdef NDEBUG
#error Assertions must remain enabled
#endif
static GCROOTS_context *ctx;
static uintptr_t needle, slot_address;
static unsigned marks, slot_seen, value_seen;
static int token;
static void *allocate(size_t size)
{
    assert(size > 0);
    return malloc(size);
}
static void *fail_allocate(size_t size)
{
    assert(size > 0);
    return NULL;
}
static void marker(void *start, void *end, int certain, int aligned)
{
    uintptr_t lo = (uintptr_t)start, hi = (uintptr_t)end;
    assert(hi >= lo && hi - lo < 8U * 1024U * 1024U);
    assert((certain == 0 || certain == 1) && (aligned == 0 || aligned == 1));
    ++marks;
    if (slot_address >= lo && slot_address < hi && hi - slot_address >= sizeof(uintptr_t))
        ++slot_seen;
    for (uintptr_t p = lo; p <= hi && hi - p >= sizeof(uintptr_t); p += sizeof(uintptr_t)) {
        uintptr_t value;
        memcpy(&value, (const void *)p, sizeof(value));
        if (value == needle)
            ++value_seen;
    }
}
static void *nested(void *arg)
{
    assert(arg == &token && GCROOTS_is_protected_context(ctx));
    return arg;
}
__attribute__((noinline)) static void *protected(void *arg)
{
    volatile uintptr_t slot[3] = {0, needle, 0};
    register uintptr_t saved __asm__("s2") = needle;
    assert(arg == &token && GCROOTS_is_protected_context(ctx));
    assert(GCROOTS_call_with_gc_ready_stack(ctx, nested, arg) == arg);
    assert(GCROOTS_is_protected_context(ctx));
    slot_address = (uintptr_t)&slot[1];
    __asm__ __volatile__("" : "+r" (saved) : : "memory");
    GCROOTS_mark(ctx);
    __asm__ __volatile__("" : "+r" (saved) : : "memory");
    assert(saved == needle && slot[1] == needle);
    assert(marks > 0 && slot_seen > 0 && value_seen > 0);
    /* Positive API check, not proof of an exclusively register-resident root. */
    assert(GCROOTS_is_protected(ctx, (void *)needle));
    slot_address = 0;
    return arg;
}
int main(void)
{
    assert(sizeof(void *) == 8);
    /* Preserve original 0.3.0/API1 macros in the 0.3.2 release. */
    assert(GCROOTS_VERSION_MAJOR == 0 && GCROOTS_VERSION_MINOR == 3);
    assert(GCROOTS_VERSION_PATCHLEVEL == 0 && GCROOTS_API_REVISION == 1);
    assert(GCROOTS_VERSION_REQUIRE(0, 3, 0));
    assert(!GCROOTS_VERSION_REQUIRE(0, 3, 1));
    assert(GCROOTS_init(fail_allocate, marker, 0) == NULL);
    ctx = GCROOTS_init(allocate, marker, 0);
    assert(ctx != NULL && !GCROOTS_is_protected_context(ctx));
    needle = (uintptr_t)malloc(64);
    assert(needle != 0 && !GCROOTS_is_protected(ctx, (void *)needle));
    for (int round = 0; round < 3; ++round) {
        marks = slot_seen = value_seen = 0;
        assert(GCROOTS_call_with_gc_ready_stack(ctx, protected, &token) == &token);
        assert(!GCROOTS_is_protected_context(ctx));
        assert(!GCROOTS_is_protected(ctx, (void *)needle));
    }
    GCROOTS_fin(ctx);
    free(ctx);
    free((void *)needle);
    puts("PASS downstream gcroots lifecycle/nesting/stack-range/snapshot rounds=3 assertions=enabled");
    return 0;
}
C
cat > run-contract.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
test -z "$root" || test "${root:0:1}" = /
sources="$root/usr/share/libgcroots/tests"
cd "$sources"
sha256sum -c SHA256SUMS
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
read -r -a cflags <<< "$(PKG_CONFIG_SYSROOT_DIR="$root" PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig" pkg-config --cflags gcroots)"
read -r -a libs <<< "$(PKG_CONFIG_SYSROOT_DIR="$root" PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig" pkg-config --libs gcroots)"
for opt in 0 2; do
    for linkage in shared static; do
        extra=()
        if test "$linkage" = static; then
            extra=(-L"$root/usr/lib64" -Wl,-Bstatic -lgcroots -Wl,-Bdynamic)
        else
            extra=("${libs[@]}")
        fi
        binary="$work/contract-$opt-$linkage"
        gcc -std=gnu11 -O"$opt" -g -UNDEBUG -Wall -Wextra -Werror "${cflags[@]}" gcroots-contract.c "${extra[@]}" -o "$binary"
        readelf -d "$binary" > "$binary.dynamic"
        if test "$linkage" = shared; then
            grep -F 'Shared library: [libgcroots.so.0]' "$binary.dynamic"
            ldd "$binary" > "$binary.ldd"
            linked=$(awk '$1 == "libgcroots.so.0" && $2 == "=>" {print $3}' "$binary.ldd")
            test -n "$linked"
            test "$(readlink -f "$linked")" = "$(readlink -f "$root/usr/lib64/libgcroots.so.0")"
        else
            if grep -F 'Shared library: [libgcroots.so.0]' "$binary.dynamic"; then
                printf 'ERROR static contract unexpectedly links shared gcroots\n' >&2
                exit 1
            fi
        fi
        "$binary"
        printf 'PASS downstream optimization=O%s linkage=%s\n' "$opt" "$linkage"
    done
done
SH

%build
# Preserve original defaults, configure checks and warnings. No source patch.
%configure CFLAGS="%{optflags} -UNDEBUG"
%make_build

%install
%make_install
find %{buildroot}%{_libdir} -name '*.la' -delete
install -d %{buildroot}%{_datadir}/libgcroots/tests
install -m 0644 gcroots-contract.c %{buildroot}%{_datadir}/libgcroots/tests/
install -m 0755 run-contract.sh %{buildroot}%{_datadir}/libgcroots/tests/
(cd %{buildroot}%{_datadir}/libgcroots/tests; sha256sum gcroots-contract.c > SHA256SUMS)

%check
# Original TESTS/check_PROGRAMS are empty. Retain check and upstream CI distcheck;
# these are original build checks, not an original semantic unit-suite claim.
make -j1 check VERBOSE=1
make -j1 distcheck VERBOSE=1
LD_LIBRARY_PATH="%{buildroot}%{_libdir}" bash %{buildroot}%{_datadir}/libgcroots/tests/run-contract.sh "%{buildroot}"

%files
%license COPYING COPYING.GPL3 m4/ax_cflags_gcc_option.m4 m4/ax_func_getcontext.m4
%doc README news.md
%{_libdir}/libgcroots.so.0*

%files devel
%{_includedir}/gcroots.h
%{_libdir}/libgcroots.so
%{_libdir}/libgcroots.a
%{_libdir}/pkgconfig/gcroots.pc
%{_datadir}/libgcroots/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.3.2-1
- Pin official tag source and retain original check/distcheck/public header.
- Add separately identified staged/installed downstream semantic checks.
