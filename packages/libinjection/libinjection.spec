# SPDX-License-Identifier: Apache-2.0
Name:           libinjection
Version:        4.0.0
Release:        1%{?dist}
Summary:        SQL injection and cross-site scripting parser library
License:        BSD-3-Clause
URL:            https://github.com/libinjection/libinjection
Source0:        libinjection-4.0.0.tar.gz
Source1:        COPYING.GPL2
Source2:        COPYING.GPL3
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  python3
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  binutils
BuildRequires:  grep
BuildRequires:  patch


%description
Libinjection tokenizes SQL injection and cross-site scripting patterns.
Detection is heuristic, not a complete application security boundary.

%package devel
Summary:        Headers and pkg-config metadata for libinjection
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Public C headers and shared-library development files.

%package static
Summary:        Static libinjection library
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
The original default static library, retained alongside the shared build.

%package tests
Summary:        Original libinjection regression corpus and installed replay
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-static%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       pkgconf
Requires:       coreutils
Requires:       findutils
Requires:       grep
Requires:       bash

%description tests
Original unmodified test drivers, unit fixtures and SQLi/XSS corpora with an
offline installed-library replay. Speed tests are not performance claims.

%prep
%autosetup -n libinjection-211782219663f889f471650150df12b623c5766e
cp -p %{SOURCE1} COPYING.GPL2
cp -p %{SOURCE2} COPYING.GPL3
# The Git archive lacks .git and the distribution-only version file.
printf '%%s\n' '%{version}' > .tarball-version
mkdir oe-tests
cp -pr tests data oe-tests/
mkdir oe-tests/src
cp -p src/reader.c src/testdriver.c src/test_stack_xss.c \
    src/test_error_handling.c src/test-driver.sh src/test-unit.sh \
    src/test-samples-sqli-negative.sh src/test-samples-sqli-positive.sh \
    src/test-samples-xss-positive.sh oe-tests/src/
cat > oe-tests/consumer.c <<'C'
#include <assert.h>
#include <string.h>
#include <libinjection.h>
int main(void) {
    char fingerprint[8];
    const char *sqli = "1' OR '1'='1";
    const char *xss = "<script>alert('xss')</script>";
    const char *html = "<p>Hello World</p>";
    assert(strcmp(libinjection_version(), "4.0.0") == 0);
    assert(libinjection_sqli("hello world 123", 15, fingerprint) == LIBINJECTION_RESULT_FALSE);
    assert(libinjection_sqli(sqli, strlen(sqli), fingerprint) == LIBINJECTION_RESULT_TRUE);
    assert(libinjection_xss(xss, strlen(xss)) == LIBINJECTION_RESULT_TRUE);
    assert(libinjection_xss(html, strlen(html)) == LIBINJECTION_RESULT_FALSE);
    assert(libinjection_xss("", 0) == LIBINJECTION_RESULT_FALSE);
    return 0;
}
C
cat > oe-tests/run-tests.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "$0")" && pwd)
libdir=${1:-/usr/lib64}
prefix=${2:-}
scratch=$(mktemp -d /tmp/libinjection-check.XXXXXXXX)
trap 'rm -rf -- "$scratch"' EXIT
cd "$root"
sha256sum -c SHA256SUMS
cp -pr src tests data "$scratch/"
cd "$scratch/src"
unset VALGRIND
export PKG_CONFIG_LIBDIR="$prefix$libdir/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="$prefix"
test "$(pkg-config --modversion libinjection)" = 4.0.0
cflags=$(pkg-config --cflags libinjection)
libs=$(pkg-config --libs libinjection)
export LD_LIBRARY_PATH="$prefix$libdir"
for pair in 'reader reader.c' 'testdriver testdriver.c' \
            'teststackxss test_stack_xss.c' 'testerrorhandling test_error_handling.c'; do
    read -r binary source <<< "$pair"
    gcc -O0 -g -UNDEBUG $cflags "$source" $libs -o "$binary"
done
# All original scripts, drivers, fixtures and expected corpus mismatch counts.
for driver in test-unit.sh test-samples-sqli-negative.sh \
              test-samples-sqli-positive.sh test-samples-xss-positive.sh \
              teststackxss testerrorhandling; do
    ./test-driver.sh "$driver"
done
# Upstream conditionally omits two allocation cases on OOM; require all 16.
grep -Eq '^Tests run: +16$' testerrorhandling.log
grep -Eq '^Tests passed: +16$' testerrorhandling.log
grep -Eq '^Tests failed: +0$' testerrorhandling.log
gcc -O0 -g -UNDEBUG $cflags "$root/consumer.c" $libs -o "$scratch/shared-consumer"
"$scratch/shared-consumer"
gcc -O0 -g -UNDEBUG $cflags "$root/consumer.c" "$prefix$libdir/libinjection.a" -o "$scratch/static-consumer"
"$scratch/static-consumer"
printf 'PASS downstream original-drivers=6 error-cases=16 consumers=2 semantic-assertions=12 skips=0\n'
SH
chmod 755 oe-tests/run-tests.sh oe-tests/src/*.sh
(cd oe-tests && find src tests data -type f -print0 | sort -z | xargs -0 sha256sum > SHA256SUMS)

%build
autoreconf -i --force
# Original stack regression requires the library's original unoptimized default.
# Preserve O0 and keep assertions active, including for installed replay.
%configure CFLAGS="%{optflags} -O0 -UNDEBUG" CXXFLAGS="%{optflags} -O0 -UNDEBUG"
%make_build

%install
%make_install
find %{buildroot} -type f -name '*.la' -delete
install -d %{buildroot}%{_datadir}/libinjection/tests
cp -pr oe-tests/. %{buildroot}%{_datadir}/libinjection/tests/

%check
make check
grep -Eq '^Tests run: +16$' src/testerrorhandling.log
grep -Eq '^Tests passed: +16$' src/testerrorhandling.log
grep -Eq '^Tests failed: +0$' src/testerrorhandling.log
bash %{buildroot}%{_datadir}/libinjection/tests/run-tests.sh %{_libdir} %{buildroot}

%files
%license COPYING COPYING.GPL2 COPYING.GPL3
%doc README.md CHANGELOG.md
%{_libdir}/libinjection.so.4*

%files devel
%{_includedir}/libinjection*.h
%{_libdir}/libinjection.so
%{_libdir}/pkgconfig/libinjection.pc

%files static
%{_libdir}/libinjection.a

%files tests
%{_datadir}/libinjection/

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.0.0-1
- Preserve original shared/static all, complete make check and installed replay.
