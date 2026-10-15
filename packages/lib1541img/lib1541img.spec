# SPDX-License-Identifier: Apache-2.0
Name:           lib1541img
Version:        1.1
Release:        1
Summary:        C library for reading and writing Commodore 1541 disk images
License:        BSD-2-Clause
URL:            https://github.com/excess-c64/lib1541img
Source0:        lib1541img-1.1.tar.gz
Source1:        zimk-31500ca556f258ab2d37d75fb8de5506cbdd5840.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  glibc-devel
BuildRequires:  pkgconf
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  rpm
BuildRequires:  tar
BuildRequires:  gzip

%description
An ISO C11 library for creating, reading and modifying Commodore 1541 D64
images, including 35/40/42-track geometry, CBM DOS files and PETSCII utilities.

%package devel
Summary:        Headers and pkg-config metadata for lib1541img
Requires:       %{name} = %{version}-%{release}

%description devel
Public C headers, shared-library linker symlink, pkg-config metadata and
separately labeled downstream verification source. Upstream's default builds
the shared library; optional staticlibs and html targets are not defaults.

%prep
%setup -q -n lib1541img-a747810f0c46d49d37711e3bade1c5c85a4b261d
tar -xf %{SOURCE1} --strip-components=1 -C zimk
test ! -e .git
test ! -e zimk/.git
cp -p zimk/LICENSE LICENSE-zimk

%build
# Complete original default target; RPM owns stripping/debug splitting.
make %{?_smp_mflags} all CC=gcc LIBDIR=build/lib OBJDIR=build/obj \
    CFLAGS="%{optflags} -std=c11" LDFLAGS="%{?build_ldflags}"
cat > verify-1541img.c <<'C'
/* SPDX-License-Identifier: BSD-2-Clause */
/* Downstream consumer checks, not an upstream test suite. */
#include <1541img/d64.h>
#include <1541img/d64reader.h>
#include <1541img/d64writer.h>
#include <1541img/track.h>
#include <1541img/sector.h>
#include <1541img/petscii.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned checks;
static void check(int ok, const char *name) {
    if (!ok) { fprintf(stderr, "FAIL downstream: %%s\n", name); exit(1); }
    ++checks;
    printf("PASS downstream: %%s\n", name);
}
int main(void) {
    const uint8_t tracks[] = {35, 40, 42};
    const long sizes[] = {174848, 196608, 205312};
    for (unsigned type = 0; type < 3; ++type) {
        D64 *disk = D64_create((D64Type)type);
        check(disk != NULL, "create image");
        check(D64_type(disk) == (D64Type)type && D64_tracks(disk) == tracks[type],
              "image type and track count");
        int geometry = 1, zeros = 1;
        for (uint8_t t = 1; t <= tracks[type]; ++t) {
            const Track *track = D64_rtrack(disk, t);
            unsigned count = t < 18 ? 21 : t < 25 ? 19 : t < 31 ? 18 : 17;
            check(track != NULL, "track exists");
            if (Track_trackNum(track) != t || Track_sectors(track) != count) geometry = 0;
            for (uint8_t s = 0; s < count; ++s) {
                const Sector *sector = Track_rsector(track, s);
                if (!sector) { geometry = 0; continue; }
                if (Sector_trackNum(sector) != t || Sector_sectorNum(sector) != s)
                    geometry = 0;
                const uint8_t *data = Sector_rcontent(sector);
                for (unsigned b = 0; b < SECTOR_SIZE; ++b) if (data[b] != 0) zeros = 0;
            }
        }
        check(geometry, "all track/sector geometry and coordinates");
        check(zeros, "new image sector bytes are zero");
        check(!D64_rtrack(disk, 0) && !D64_rtrack(disk, tracks[type]+1) &&
              !D64_rsector(disk, 1, 21), "invalid coordinates rejected");
        Sector *marked = D64_sector(disk, 18, 0);
        check(marked != NULL, "mutable sector access");
        uint8_t *bytes = Sector_content(marked);
        for (unsigned b = 0; b < SECTOR_SIZE; ++b) bytes[b] = (uint8_t)(b ^ 0xa5);
        FILE *file = tmpfile();
        check(file != NULL, "temporary stream");
        check(writeD64(file, disk) == 0 && ftell(file) == sizes[type],
              "write exact image size");
        rewind(file);
        D64 *copy = readD64(file);
        check(copy && D64_type(copy) == (D64Type)type && D64_tracks(copy) == tracks[type],
              "read image type and track count");
        const Sector *copysector = D64_rsector(copy, 18, 0);
        check(copysector && memcmp(Sector_rcontent(copysector), bytes, SECTOR_SIZE) == 0,
              "sector bytes survive image roundtrip");
        check(fclose(file) == 0, "close image stream");
        D64_destroy(copy);
        D64_destroy(disk);
    }
    check(!D64_create((D64Type)3) && !Track_create(0) && !Track_create(43),
          "invalid constructors rejected");
    char petscii[32] = {0}, utf8[32] = {0};
    check(petscii_fromUtf8(petscii, sizeof petscii, "ABC 123", 7, PC_FORCEUPPER, 1, '?') == 8
          && memcmp(petscii, "ABC 123", 8) == 0, "UTF8 to upper PETSCII");
    check(petscii_toUtf8(utf8, sizeof utf8, petscii, 7, 0, 1, "?", " ") == 8
          && strcmp(utf8, "ABC 123") == 0, "upper PETSCII to UTF8");
    printf("{\"suite\":\"downstream-1541img-consumer\",\"checks\":%%u,\"skips\":0,\"status\":\"passed\"}\n", checks);
    return 0;
}
C

%install
make install CC=gcc LIBDIR=build/lib OBJDIR=build/obj \
    CFLAGS="%{optflags} -std=c11" LDFLAGS="%{?build_ldflags}" \
    DESTDIR="%{buildroot}" prefix=%{_prefix} libdir=%{_libdir} \
    includedir=%{_includedir} pkgconfigdir=%{_libdir}/pkgconfig
install -Dpm0644 verify-1541img.c %{buildroot}%{_datadir}/lib1541img/verify-1541img.c

%check
# No original check/test target is declared; preserve the complete default
# build and run separately labeled downstream consumers without network.
make all CC=gcc LIBDIR=build/lib OBJDIR=build/obj \
    CFLAGS="%{optflags} -std=c11" LDFLAGS="%{?build_ldflags}"
gcc %{optflags} -std=c11 -Iinclude verify-1541img.c -Lbuild/lib -l1541img -o verify-source
LD_LIBRARY_PATH="$PWD/build/lib" ./verify-source
test "$(PKG_CONFIG_LIBDIR=%{buildroot}%{_libdir}/pkgconfig pkg-config --modversion 1541img)" = 1.1.0
PKG_CONFIG_LIBDIR=%{buildroot}%{_libdir}/pkgconfig PKG_CONFIG_SYSROOT_DIR=%{buildroot} \
    pkg-config --cflags --libs 1541img > staged-flags
gcc %{optflags} -std=c11 verify-1541img.c $(cat staged-flags) -o verify-staged
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ./verify-staged

%files
%license LICENSE.txt LICENSE-zimk
%doc %{_datadir}/doc/1541img/
%{_libdir}/lib1541img.so.1
%{_libdir}/lib1541img.so.1.1.0

%files devel
%{_includedir}/1541img/
%{_libdir}/lib1541img.so
%{_libdir}/pkgconfig/1541img.pc
%{_datadir}/lib1541img/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Own all three documents installed by upstream's original install target.
- Pin official v1.1 and exact zimk submodule; preserve default shared build.
- Add source, staged and installed downstream disk-image consumer checks.
