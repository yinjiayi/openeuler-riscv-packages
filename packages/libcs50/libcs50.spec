# SPDX-License-Identifier: Apache-2.0
Name:           libcs50
Version:        11.0.4
Release:        1%{?dist}
Summary:        CS50 C library for checked line-oriented user input
License:        BSD-3-Clause AND GPL-3.0-only
URL:            https://github.com/cs50/libcs50
Source0:        libcs50-11.0.4.tar.gz
Patch0:         0001-update-original-samples-to-required-format-argument.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  diffutils
BuildRequires:  coreutils
BuildRequires:  patch


%description
CS50 provides checked line-oriented input functions for C. The complete
BSD notices and repository GPLv3 license are retained, not stale fpm metadata.

%package devel
Summary:        Headers, static library and reproducible checks for libcs50
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Original header, static archive, seven manuals, full C implementation and
both upstream samples, plus separately identified downstream input checks.

%prep
%autosetup -n libcs50-37709b01398c9d72a112b864f12c789a910c61fb -p1
# Literal complete BSD copyright, conditions and disclaimer.
sed -n '1,/^ \*\//p' src/cs50.c > COPYING.BSD-3-Clause
test -s COPYING.BSD-3-Clause

%build
# Preserve all default outputs and warning flags. Multiple outputs share a rule.
make -j1 all CC=%{__cc} CFLAGS='%{optflags} -Wall -Wextra -Werror -pedantic -std=c11'
# Upstream normally obtains the SONAME link from install-time ldconfig.
ln -sfn libcs50.so.%{version} build/lib/libcs50.so.11
cat > verify-input.c <<'C'
/* SPDX-License-Identifier: Apache-2.0
 * Downstream checks, not an upstream registered test suite. */
#include <cs50.h>
#include <stdio.h>
#include <string.h>
static unsigned checks;
static int check(int pass, const char *name)
{
    if (!pass) { fprintf(stderr, "FAIL %%s\n", name); return 0; }
    ++checks;
    return 1;
}
#define CHECK(v, n) do { if (!check((v), (n))) return 1; } while (0)
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    if (!strcmp(argv[1], "values")) {
        CHECK(get_int(NULL) == -42, "int-negative");
        CHECK(get_char(NULL) == 'Z', "char");
        CHECK(get_long(NULL) == 2147483648L, "long-64-bit");
        CHECK(get_long_long(NULL) == 9223372036854775806LL, "long-long");
        CHECK(get_float(NULL) == 1.25f, "float");
        CHECK(get_double(NULL) == -2.5, "double");
        string s = get_string(NULL);
        CHECK(s != NULL && !strcmp(s, "with spaces"), "string-spaces");
    } else if (!strcmp(argv[1], "eof")) {
        CHECK(get_int(NULL) == INT_MAX, "int-eof");
        CHECK(get_char(NULL) == CHAR_MAX, "char-eof");
        CHECK(get_long(NULL) == LONG_MAX, "long-eof");
        CHECK(get_long_long(NULL) == LLONG_MAX, "long-long-eof");
        CHECK(get_float(NULL) == FLT_MAX, "float-eof");
        CHECK(get_double(NULL) == DBL_MAX, "double-eof");
        CHECK(get_string(NULL) == NULL, "string-eof");
    } else if (!strcmp(argv[1], "endings")) {
        const char *want[] = {"alpha", "beta", "gamma", "", "last"};
        for (unsigned i = 0; i < sizeof(want)/sizeof(want[0]); ++i) {
            string s = get_string(NULL);
            CHECK(s != NULL && !strcmp(s, want[i]), "line-ending-or-final-line");
        }
        CHECK(get_string(NULL) == NULL, "final-eof");
    } else return 2;
    printf("PASS downstream-input %%s %%u\n", argv[1], checks);
    return 0;
}
C
cat > run-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
export LC_ALL=C
include=$1; library=$2; sources=$3; phase=$4
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
run() {
    if [[ $phase == installed ]]; then
        env -u LD_LIBRARY_PATH -u LD_PRELOAD timeout 15 "$@"
    else
        env -u LD_PRELOAD LD_LIBRARY_PATH="$library" timeout 15 "$@"
    fi
}
for link in shared static; do
    if [[ $link == shared ]]; then libs=(-L"$library" -lcs50); else libs=("$library/libcs50.a"); fi
    for name in get_int hackerrank; do
        gcc -std=c11 -Wall -Wextra -pedantic -I"$include" "$sources/$name.c" "${libs[@]}" -o "$work/$name"
    done
    gcc -std=c11 -Wall -Wextra -pedantic -I"$include" "$sources/verify-input.c" "${libs[@]}" -o "$work/verify-input"
    printf 'not-an-int\n2147483647\n42\n-7\n' | run "$work/get_int" > "$work/get_int.actual"
    printf '42\nFoo: -7\n' > "$work/get_int.expected"
    diff -u "$work/get_int.expected" "$work/get_int.actual"
    echo "PASS original-sample $phase $link get_int"
    printf 'world\n' | run "$work/hackerrank" > "$work/hackerrank.actual"
    printf 'hello, world\n' > "$work/hackerrank.expected"
    diff -u "$work/hackerrank.expected" "$work/hackerrank.actual"
    echo "PASS original-sample $phase $link hackerrank"
    printf '%%s\n' '-42' 'Z' '2147483648' '9223372036854775806' '1.25' '-2.5' 'with spaces' | run "$work/verify-input" values
    run "$work/verify-input" eof < /dev/null
    printf 'alpha\r\nbeta\rgamma\n\nlast' | run "$work/verify-input" endings
    echo "PASS downstream-input-phase $phase $link checks=20 samples=2 skips=0"
done
SH
chmod 755 run-tests.sh
mkdir -p test-payload
cp tests/get_int.c tests/hackerrank.c verify-input.c run-tests.sh test-payload/
(cd test-payload && sha256sum get_int.c hackerrank.c verify-input.c run-tests.sh > SHA256SUMS)

%install
# Upstream DESTDIR is a prefix and hardcodes lib/ldconfig, not RPM DESTDIR.
# Stage its complete default output in lib64 without host ldconfig.
install -d %{buildroot}%{_libdir} %{buildroot}%{_includedir} %{buildroot}%{_mandir}/man3
install -m755 build/lib/libcs50.so.%{version} %{buildroot}%{_libdir}/
ln -s libcs50.so.%{version} %{buildroot}%{_libdir}/libcs50.so.11
ln -s libcs50.so.11 %{buildroot}%{_libdir}/libcs50.so
install -m644 build/lib/libcs50.a %{buildroot}%{_libdir}/
install -m644 build/include/cs50.h %{buildroot}%{_includedir}/
install -m644 docs/*.3.gz %{buildroot}%{_mandir}/man3/
install -d %{buildroot}%{_datadir}/libcs50/tests %{buildroot}%{_datadir}/libcs50/src
install -m644 src/cs50.c %{buildroot}%{_datadir}/libcs50/src/
install -m644 test-payload/*.c test-payload/SHA256SUMS %{buildroot}%{_datadir}/libcs50/tests/
install -m755 test-payload/run-tests.sh %{buildroot}%{_datadir}/libcs50/tests/

%check
# No registered upstream check target. Execute both shipped original samples
# plus explicitly downstream checks; never label an empty test target success.
(cd test-payload && sha256sum -c SHA256SUMS)
bash test-payload/run-tests.sh "$PWD/build/include" "$PWD/build/lib" "$PWD/test-payload" source
bash test-payload/run-tests.sh "%{buildroot}%{_includedir}" "%{buildroot}%{_libdir}" "%{buildroot}%{_datadir}/libcs50/tests" staged

%files
%license LICENSE COPYING.BSD-3-Clause
%doc README.md
%{_libdir}/libcs50.so.11
%{_libdir}/libcs50.so.%{version}

%files devel
%{_includedir}/cs50.h
%{_libdir}/libcs50.so
%{_libdir}/libcs50.a
%{_mandir}/man3/get_*.3*
%{_datadir}/libcs50/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 11.0.4-1
- Pin the stable source and preserve all default outputs and both samples.
- Add source, staged and installed shared/static input checks and full notices.
