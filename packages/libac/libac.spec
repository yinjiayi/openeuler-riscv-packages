# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 061bdbb82ffa76fdf91e78920ca142d2b8a40211
Name:           libac
Version:        2.0.0
Release:        1%{?dist}
Summary:        Miscellaneous C utility library
License:        LGPL-2.1-only AND LGPL-2.1-or-later AND BSD-3-Clause AND Apache-2.0
URL:            https://github.com/ac000/libac
Source0:        libac-2.0.0.tar.gz
Source1:        COPYING.APACHE2
Source2:        COPYING.GPL2
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
# Match the fixed SP3 glibc-devel/static-provider closure; see README.
BuildRequires:  libxcrypt-devel = 4.4.36-3.oe2403sp3
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  gawk
BuildRequires:  grep
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  rpm

%description
A C library of miscellaneous utility functions, including queues, circular
buffers, strings, JSON, networking and time helpers.

%package devel
Summary:        Public header and shared-library linker interface for libac
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc glibc-devel bash coreutils binutils grep gawk
Requires:       libxcrypt-devel = 4.4.36-3.oe2403sp3

%description devel
The unmodified public header, shared-library linker interface and a separately
labelled offline, fail-first downstream consumer. No static library or invented
pkg-config interface is installed.

%prep
%autosetup -n %{name}-%{upstream_commit}
cp -p %{SOURCE1} COPYING.APACHE2
cp -p %{SOURCE2} COPYING.GPL2
cat > contract.c <<'C'
/* SPDX-License-Identifier: Apache-2.0 */
#define _GNU_SOURCE
#include <libac.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#ifdef NDEBUG
#error Assertions must not be disabled
#endif
static unsigned int checks;
#define CHECK(x) do { if (!(x)) { fputs("FAIL " #x "\n", stderr); exit(1); } ++checks; } while (0)
int main(void)
{
    int values[] = {11, 22, 33, 44};
    char **parts;
    ac_queue_t *q;
    ac_circ_buf_t *c;
    ac_jsonw_t *j;
    const char expected[] = "{\n    \"text\": \"a\\\"\\\\\\n\",\n    \"count\": -7,\n    \"ok\": true,\n    \"none\": null\n}";
    CHECK(LIBAC_MAJOR_VERSION == 2 && LIBAC_MINOR_VERSION == 0 && LIBAC_MICRO_VERSION == 0);
    q = ac_queue_new(); CHECK(q != NULL);
    CHECK(ac_queue_nr_items(q) == 0 && ac_queue_pop(q) == NULL);
    for (unsigned int i = 0; i < 4; ++i) CHECK(ac_queue_push(q, &values[i]) == 0);
    CHECK(ac_queue_nr_items(q) == 4);
    for (unsigned int i = 0; i < 4; ++i) CHECK(ac_queue_pop(q) == &values[i]);
    CHECK(ac_queue_nr_items(q) == 0 && ac_queue_pop(q) == NULL);
    CHECK(ac_queue_push(NULL, &values[0]) == -1 && ac_queue_pop(NULL) == NULL);
    ac_queue_destroy(q, NULL);
    CHECK(ac_circ_buf_new(3, sizeof(int)) == NULL);
    c = ac_circ_buf_new(4, sizeof(int)); CHECK(c != NULL);
    CHECK(ac_circ_buf_count(c) == 0 && ac_circ_buf_pop(c) == NULL);
    for (unsigned int i = 0; i < 3; ++i) CHECK(ac_circ_buf_push(c, &values[i]) == 0);
    CHECK(ac_circ_buf_count(c) == 3 && ac_circ_buf_push(c, &values[3]) == -1);
    CHECK(*(int *)ac_circ_buf_pop(c) == values[0]);
    CHECK(ac_circ_buf_push(c, &values[3]) == 0);
    for (unsigned int i = 1; i < 4; ++i) CHECK(*(int *)ac_circ_buf_pop(c) == values[i]);
    CHECK(ac_circ_buf_pop(c) == NULL && ac_circ_buf_count(c) == 0);
    CHECK(ac_circ_buf_push(c, &values[0]) == 0);
    ac_circ_buf_reset(c); CHECK(ac_circ_buf_count(c) == 0);
    ac_circ_buf_destroy(c);
    parts = ac_str_split("a,,b", ',', AC_STR_SPLIT_ALWAYS);
    CHECK(parts != NULL);
    CHECK(parts[0] && strcmp(parts[0], "a") == 0);
    CHECK(parts[1] && strcmp(parts[1], "") == 0);
    CHECK(parts[2] && strcmp(parts[2], "b") == 0 && parts[3] == NULL);
    ac_str_freev(parts);
    parts = ac_str_split("abc", ',', AC_STR_SPLIT_STRICT);
    CHECK(parts != NULL && parts[0] == NULL); ac_str_freev(parts);
    errno = 0; parts = ac_str_split("a,b", ',', 2);
    CHECK(parts == NULL && errno == EINVAL);
    CHECK(ac_str_levenshtein("kitten", "sitting") == 3);
    CHECK(ac_str_levenshtein("equal", "equal") == 0);
    j = ac_jsonw_init(); CHECK(j != NULL);
    ac_jsonw_add_str(j, "text", "a\"\\\n");
    ac_jsonw_add_int(j, "count", -7);
    ac_jsonw_add_bool(j, "ok", true);
    ac_jsonw_add_null(j, "none"); ac_jsonw_end(j);
    CHECK(strcmp(ac_jsonw_get(j), expected) == 0);
    CHECK(ac_jsonw_len(j) == strlen(expected)); ac_jsonw_free(j);
    printf("PASS downstream-libac checks=%u skips=0\n", checks);
    return 0;
}
C

%build
# Environment CFLAGS are extended by upstream's += rules. Keep every default
# warning, hardening flag, library source and original example test target.
export CFLAGS="%{optflags} -UNDEBUG -Werror"
%make_build V=1
test -x src/test

%install
install -d %{buildroot}%{_libdir} %{buildroot}%{_includedir} \
    %{buildroot}%{_datadir}/%{name}/tests
install -pm0755 src/libac.so.2.0.0 %{buildroot}%{_libdir}/
ln -s libac.so.2.0.0 %{buildroot}%{_libdir}/libac.so.2
ln -s libac.so.2.0.0 %{buildroot}%{_libdir}/libac.so
install -pm0644 src/include/libac.h %{buildroot}%{_includedir}/
install -pm0644 contract.c %{buildroot}%{_datadir}/%{name}/tests/
sha256sum contract.c > %{buildroot}%{_datadir}/%{name}/tests/SHA256SUMS
cat > %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
root=${1:-}
test -z "$root" || test -d "$root/usr/lib64"
fixtures="$root/usr/share/libac/tests"
cd "$fixtures"
sha256sum -c SHA256SUMS
expected=$(readlink -f "$root/usr/lib64/libac.so.2")
test -s "$expected"
workdir=$(mktemp -d /tmp/libac-contract.XXXXXXXX)
trap 'rm -f "$workdir/test-0" "$workdir/test-2"; rmdir "$workdir"' EXIT
if test -n "$root"; then
    export LD_LIBRARY_PATH="$root/usr/lib64"
else
    unset LD_LIBRARY_PATH
fi
for opt in 0 2; do
    gcc -O"$opt" -g -UNDEBUG -Wall -Wextra -Werror -std=gnu11 \
        -I"$root/usr/include" contract.c -L"$root/usr/lib64" -lac \
        -o "$workdir/test-$opt"
    readelf -d "$workdir/test-$opt" | grep -F 'Shared library: [libac.so.2]'
    if readelf -d "$workdir/test-$opt" | grep -E '\((RPATH|RUNPATH)\)'; then
        echo 'Unexpected embedded library search path' >&2
        exit 1
    fi
    actual=$(ldd "$workdir/test-$opt" | awk '$1 == "libac.so.2" {print $3}')
    test -n "$actual"
    test "$(readlink -f "$actual")" = "$expected"
    "$workdir/test-$opt"
    echo "PASS downstream-libac opt=$opt"
done
SH
chmod 0755 %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh

%check
# Upstream's test target compiles a print-oriented example and does not execute
# it. Preserve that target, without claiming its compilation as test passes.
make -j1 test V=1
# Distinct deterministic shared-library checks; no external DNS or /tmp/services.
bash %{buildroot}%{_datadir}/%{name}/tests/run-contract.sh %{buildroot}

%files
%license COPYING COPYING.GPL2 COPYING.APACHE2
%license src/platform/common/random_r.c src/platform/common/twalk_r.c
%license src/platform/freebsd/tdestroy.c
%doc README.rst
%{_libdir}/libac.so.2*

%files devel
%{_includedir}/libac.h
%{_libdir}/libac.so
%{_datadir}/%{name}/tests/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Pin official v2.0.0 source and preserve default library/example build.
- Supply complete license texts and separate offline shared-ABI checks.
