# SPDX-License-Identifier: Apache-2.0
Name:           libhaiku
Version:        2.0.2
Release:        1
Summary:        Poetic error messages
License:        ISC
URL:            https://codeberg.org/maandree/libhaiku
Source0:        https://codeberg.org/maandree/libhaiku/archive/%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
A collection of three-line poetic error messages with errno selection
and optional prefixes for each printed line.

%package devel
Summary:        Public header, manuals and static library for libhaiku
Requires:       %{name} = %{version}-%{release}

%description devel
The unchanged public header, manuals, shared linker name and static library.

%package tests
Summary:        Checksum-bound original source for downstream libhaiku checks
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
The original source archive for installed shared and static library checks.
Upstream ships no check target or test driver; downstream functional checks
are not an upstream suite or evidence of randomness quality or thread safety.

%prep
%autosetup -n libhaiku

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags}"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libhaiku/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libhaiku/qa/libhaiku-%{version}.tar.gz

%check
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libhaiku/qa/libhaiku-2.0.2.tar.gz"
    echo '84f70765149da30738f2f5d2a372d9fd4c3cc061c06a596dfa605f04c459a094  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libhaiku.h" "$root/usr/include/libhaiku.h"
    cd "$work"
    cat > api.c <<'EOF'
#define _POSIX_C_SOURCE 200809L
#include <libhaiku.h>
#include <assert.h>
#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
static void poem(const char *s) {
    int n = 0;
    const char *line = s;
    assert(s && *s);
    for (; *s; ++s) if (*s == '\n') {
        assert(s > line);
        ++n; line = s + 1;
    }
    assert(n == 3 && line == s);
}
static void printed(const char *prefix, int wrapper, int err) {
    FILE *f = tmpfile();
    int saved;
    char out[4096];
    size_t n;
    assert(f && fflush(stderr) == 0);
    saved = dup(STDERR_FILENO); assert(saved >= 0);
    assert(dup2(fileno(f), STDERR_FILENO) == STDERR_FILENO);
    errno = err;
    if (wrapper) libhaiku_perror(prefix); else libhaiku_perror2(prefix, err);
    assert(!ferror(stderr) && fflush(stderr) == 0);
    assert(dup2(saved, STDERR_FILENO) == STDERR_FILENO && close(saved) == 0);
    assert(fseek(f, 0, SEEK_SET) == 0);
    n = fread(out, 1, sizeof(out) - 1, f);
    assert(!ferror(f) && feof(f) && n > 0);
    out[n] = 0; assert(fclose(f) == 0); poem(out);
    if (prefix && *prefix) {
        const char *p = out;
        size_t len = strlen(prefix);
        for (int i = 0; i < 3; ++i) {
            assert(!strncmp(p, prefix, len) && p[len] == ':' && p[len+1] == ' ');
            p = strchr(p, '\n') + 1;
        }
    }
    if (err == ENETDOWN) assert(strstr(out, "The network is down.\n"));
}
int main(void) {
    int generic;
    const int specific[] = {ENETDOWN, ENOMEM, ENOENT, EACCES, EPIPE};
    const int fallback[] = {-1, INT_MAX};
    for (int repeat = 0; repeat < 32; ++repeat) {
        poem(libhaiku_generic());
        for (size_t i = 0; i < sizeof(specific)/sizeof(*specific); ++i) {
            generic = -9; poem(libhaiku_strerror(specific[i], &generic));
            assert(generic == 0); poem(libhaiku_strerror(specific[i], NULL));
        }
        for (size_t i = 0; i < sizeof(fallback)/sizeof(*fallback); ++i) {
            generic = -9; poem(libhaiku_strerror(fallback[i], &generic));
            assert(generic == 1);
        }
    }
    printed("qa", 0, ENETDOWN); printed("qa", 1, ENETDOWN);
    printed(NULL, 0, -1); printed("", 0, INT_MAX);
    printed(NULL, 1, ENETDOWN); printed("", 1, ENETDOWN);
    puts("PASS libhaiku four APIs, errno/fallback, three lines and stderr prefixes");
    return 0;
}
EOF
    gcc -std=c99 -O2 -g -Wall -Wextra -Werror -fno-inline -I"$root/usr/include" api.c -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lhaiku -o api-shared
    gcc -std=c99 -O2 -g -Wall -Wextra -Werror -fno-inline -I"$root/usr/include" api.c "$root/usr/lib64/libhaiku.a" -o api-static
    LD_LIBRARY_PATH="$root/usr/lib64" ./api-shared
    ./api-static
    readelf -d api-shared | grep 'Shared library: \[libhaiku.so.2\]'
    echo 'PASS libhaiku downstream checks against installed shared and static libraries'
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libhaiku.so.2*

%files devel
%license LICENSE
%{_includedir}/libhaiku.h
%{_libdir}/libhaiku.so
%{_libdir}/libhaiku.a
%{_mandir}/man3/libhaiku_*.3*
%{_mandir}/man7/libhaiku.7*

%files tests
%license LICENSE
%{_datadir}/libhaiku/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 2.0.2-1
- Preserve original defaults and add installed shared/static functional checks.
