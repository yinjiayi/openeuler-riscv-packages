# SPDX-License-Identifier: Apache-2.0
Name:           libred
Version:        1.1.3
Release:        1
Summary:        Solar elevation and blackbody colour library
License:        ISC
URL:            https://codeberg.org/maandree/libred
Source0:        https://codeberg.org/maandree/libred/archive/%{version}.tar.gz
Patch0:         0001-order-shared-colour-table-generation.patch
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  sed
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  coreutils
BuildRequires:  diffutils

%description
C library for solar elevation and blackbody colour calculations.

%package devel
Summary:        Public header, static library and manuals for libred
Requires:       %{name} = %{version}-%{release}

%description devel
Original public header, shared linker name, static library and manual pages.

%package tests
Summary:        Package-added libred functional ABI consumer and source archive
Requires:       %{name}-devel = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       binutils
Requires:       tar
Requires:       gzip
Requires:       coreutils
Requires:       diffutils

%description tests
Package-added shared/static functional consumer and fixed original source archive.
Upstream provides no check target; this is not an original upstream test suite.

%prep
%autosetup -n libred -p1
cat > consumer.c <<'LIBRED_CONSUMER_EOF'
/* SPDX-License-Identifier: ISC
 * Copyright (c) 2026 yinjiayi
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
/* Package-added functional ABI checks, not an upstream or scientific suite. */
#include <libred.h>
#include <errno.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define REQUIRE(c) do { if (!(c)) { fprintf(stderr, "FAIL line %%d: %%s\n", __LINE__, #c); exit(1); } } while (0)

int main(void)
{
    double r, g, b, x, y, x0, y0, x1, y1, dx, dy, t, elevation;
    long temperature;
    errno = 0;
    REQUIRE(libred_get_colour(999, &r, &g, &b) == -1 && errno == EDOM);
    errno = 0;
    REQUIRE(libred_get_colour_xy(999, &x, &y) == -1 && errno == EDOM);
    /* Exercise every table row and an interpolated point in every interval. */
    for (temperature = 1000; temperature <= 40000; temperature += 50) {
        REQUIRE(libred_get_colour(temperature, &r, &g, &b) == 0);
        REQUIRE(isfinite(r) && isfinite(g) && isfinite(b));
        REQUIRE(r >= 0 && r <= 1.000000000001 && g >= 0 && g <= 1.000000000001 && b >= 0 && b <= 1.000000000001);
        REQUIRE(libred_get_colour_xy(temperature, &x, &y) == 0);
        REQUIRE(isfinite(x) && isfinite(y) && x > 0 && y > 0 && x + y < 1);
    }
    REQUIRE(libred_get_colour(6500, &r, &g, &b) == 0);
    REQUIRE(fabs(r - 1) < 1e-12 && fabs(g - 1) < 1e-12 && fabs(b - 1) < 1e-12);
    REQUIRE(libred_get_colour_xy(6500, &x0, &y0) == 0);
    REQUIRE(fabs(x0 - 0.312727) < 1e-12 && fabs(y0 - 0.329023) < 1e-12);
    t = libred_get_temperature_xy(x0, y0, &dx, &dy);
    REQUIRE(isfinite(t) && fabs(t - 6500) < 1e-6 && fabs(dx) < 1e-12 && fabs(dy) < 1e-12);
    REQUIRE(fabs(libred_get_temperature_xy(x0, y0, NULL, NULL) - 6500) < 1e-6);
    t = libred_get_temperature(r, g, b, NULL, NULL, NULL, NULL);
    REQUIRE(isfinite(t) && t >= 1000 && t <= 40000);
    REQUIRE(libred_get_colour_xy(6600, &x1, &y1) == 0);
    REQUIRE(libred_get_colour_xy(6550, &x, &y) == 0);
    REQUIRE(fabs(x - (x0 + x1) / 2) < 1e-12 && fabs(y - (y0 + y1) / 2) < 1e-12);
    REQUIRE(libred_get_colour_xy(40000, &x0, &y0) == 0);
    REQUIRE(libred_get_colour_xy(50000, &x, &y) == 0);
    REQUIRE(fabs(x - x0) < 1e-12 && fabs(y - y0) < 1e-12);
    REQUIRE(libred_solar_elevation(0, 0, &elevation) == 0);
    REQUIRE(isfinite(elevation) && elevation >= -90 && elevation <= 90);
    REQUIRE(LIBRED_IS_NIGHTTIME(-30) && LIBRED_IS_DAYTIME(30));
    REQUIRE(LIBRED_IS_BLUE_HOUR(-5) && LIBRED_IS_GOLDEN_HOUR(0));
    puts("PASS libred package-added full-table/interpolation/errors/shared-static functional consumer");
    return 0;
}
LIBRED_CONSUMER_EOF

%build
%make_build CC="gcc -std=c99" CFLAGS="%{optflags} -Wall" LDFLAGS="%{?build_ldflags} -lm"

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
install -d %{buildroot}%{_datadir}/libred/qa
install -m 0644 %{SOURCE0} %{buildroot}%{_datadir}/libred/qa/libred-%{version}.tar.gz
install -m 0644 consumer.c %{buildroot}%{_datadir}/libred/qa/consumer.c

%check
# The unchanged upstream Makefile has no check/test target; do not invent one.
run_installed_tests() (
    set -eux
    root=$1
    archive="$root/usr/share/libred/qa/libred-1.1.3.tar.gz"
    echo '8d08527ae4892693bc9e1896f67c0d0538e46569bd3c9515f313e0f9c7a245fa  '"$archive" | sha256sum -c -
    work=$(mktemp -d)
    trap 'rm -rf -- "$work"' EXIT
    tar -xzf "$archive" -C "$work" --strip-components=1
    cmp -- "$work/libred.h" "$root/usr/include/libred.h"
    cd "$work"
    gcc -std=c99 -O2 -g -Wall -I"$root/usr/include" "$root/usr/share/libred/qa/consumer.c" -L"$root/usr/lib64" -Wl,-rpath,"$root/usr/lib64" -lred -lm -o consumer-shared
    readelf -d consumer-shared | grep 'Shared library: \[libred.so.1\]'
    gcc -std=c99 -O2 -g -Wall -I"$root/usr/include" "$root/usr/share/libred/qa/consumer.c" "$root/usr/lib64/libred.a" -lm -o consumer-static
    LD_LIBRARY_PATH="$root/usr/lib64" ./consumer-shared
    ./consumer-static
)
run_installed_tests '%{buildroot}'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README
%{_libdir}/libred.so.1*

%files devel
%license LICENSE
%{_includedir}/libred.h
%{_libdir}/libred.so
%{_libdir}/libred.a
%{_mandir}/man0/libred.h.0*
%{_mandir}/man3/libred_*.3*
%{_mandir}/man7/libred.7*

%files tests
%license LICENSE
%{_datadir}/libred/

%changelog
* Mon Oct 19 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.3-1
- Preserve upstream all and add staged/installed shared/static functional checks.
