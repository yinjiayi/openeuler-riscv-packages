# SPDX-License-Identifier: Apache-2.0
Name:           libudfread
Version:        1.2.0
Release:        1%{?dist}
Summary:        Userspace UDF filesystem image reader
License:        LGPL-2.1-or-later AND MIT
URL:            https://code.videolan.org/videolan/libudfread
Source0:        libudfread-1.2.0.tar.xz
Source1:        GPL-2.0.txt
Source2:        MIT.txt
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  genisoimage
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  meson >= 0.60.0
BuildRequires:  ninja-build
BuildRequires:  pkgconf-pkg-config
BuildRequires:  sed
Requires:       bash
Requires:       coreutils

%description
Read UDF filesystem images through a userspace library. Preserve upstream's
default shared and static libraries, optional pthread probe and original
Meson test entry point. Additional regressions use regular image files only.

%prep
%autosetup -n libudfread-1.2.0 -p1
# Preserve every one of the 26 original members, including all per-file notices.
find . -path ./license-notices -prune -o -type f -print | while IFS= read -r original; do
    mkdir -p "license-notices/${original%/*}"
    cp -p "$original" "license-notices/$original.notice"
done
cp -p %{SOURCE1} license-notices/GPL-2.0.txt
cp -p %{SOURCE2} license-notices/MIT.txt
(cd license-notices; find . -type f -exec sha256sum {} + | LC_ALL=C sort) > notice-checksums
cp notice-checksums license-notices/SHA256SUMS
find license-notices -type f -exec chmod 0644 {} +
test "$(find license-notices -type f | wc -l)" -eq 29
cat > api-smoke.c <<'LIBUDFREAD_API_EOF'
/* Copyright 2026 openEuler RISC-V package contributors.
 * SPDX-License-Identifier: MIT
 * The complete MIT permission and warranty notice accompanies this source in
 * license-notices/MIT.txt. This driver is independent of upstream test code.
 */
#include <udfread/udfread.h>
#include <udfread/udfread-version.h>
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char unit[] = "libudfread test payload\n";
static const char nested[] = "nested UDF contents\n";
enum { repeats = 200 };

int main(int argc, char **argv) {
    assert(argc == 2);
    int major = -1, minor = -1, micro = -1;
    udfread_get_version(&major, &minor, &micro);
    assert(major == 1 && minor == 2 && micro == 0);
    udfread *u = udfread_init();
    assert(u != NULL);
    assert(udfread_open(u, NULL) < 0);
    assert(udfread_open_input(u, NULL) < 0);
    assert(udfread_file_size(NULL) == -1);
    puts("API case1 version-and-invalid-input PASS");

    assert(udfread_open(u, argv[1]) == 0);
    const char *volume = udfread_get_volume_id(u);
    assert(volume != NULL && strcmp(volume, "UDFREAD_TEST") == 0);
    unsigned char volume_set[128];
    assert(udfread_get_volume_set_id(u, volume_set, sizeof(volume_set)) == 128);
    puts("API case2 regular-image-volume PASS");

    UDFDIR *root = udfread_opendir(u, "/");
    assert(root != NULL);
    struct udfread_dirent entry;
    int payload_seen = 0, sub_seen = 0;
    while (udfread_readdir(root, &entry) != NULL) {
        if (strcmp(entry.d_name, "payload.txt") == 0) {
            assert(entry.d_type == UDF_DT_REG); payload_seen++;
        }
        if (strcmp(entry.d_name, "sub") == 0) {
            assert(entry.d_type == UDF_DT_DIR); sub_seen++;
        }
    }
    assert(payload_seen == 1 && sub_seen == 1);
    udfread_rewinddir(root);
    assert(udfread_readdir(root, &entry) != NULL);
    UDFDIR *sub = udfread_opendir_at(root, "sub");
    assert(sub != NULL);
    assert(udfread_file_open(u, "missing-file") == NULL);
    puts("API case3 directory-and-missing-file PASS");

    const size_t size = (sizeof(unit) - 1) * repeats;
    unsigned char *expected = malloc(size), *actual = malloc(size + 1);
    assert(expected != NULL && actual != NULL && size > 4096);
    for (size_t i = 0; i < repeats; i++)
        memcpy(expected + i * (sizeof(unit) - 1), unit, sizeof(unit) - 1);
    UDFFILE *f = udfread_file_open(u, "/payload.txt");
    assert(f != NULL && udfread_file_size(f) == (int64_t)size);
    assert(udfread_file_tell(f) == 0);
    size_t got = 0;
    while (got < size) {
        ssize_t n = udfread_file_read(f, actual + got, size - got);
        assert(n > 0 && (size_t)n <= size - got); got += (size_t)n;
    }
    assert(memcmp(actual, expected, size) == 0);
    assert(udfread_file_tell(f) == (int64_t)size);
    assert(udfread_file_read(f, actual, 1) == 0);
    puts("API case4 multi-block-byte-stream PASS");

    assert(udfread_file_seek(f, 2047, UDF_SEEK_SET) == 2047);
    assert(udfread_file_read(f, actual, 7) == 7);
    assert(memcmp(actual, expected + 2047, 7) == 0);
    assert(udfread_file_seek(f, -4, UDF_SEEK_CUR) == 2050);
    assert(udfread_file_seek(f, -4, UDF_SEEK_END) == (int64_t)size - 4);
    assert(udfread_file_read(f, actual, 4) == 4);
    assert(memcmp(actual, expected + size - 4, 4) == 0);
    assert(udfread_file_seek(f, -1, UDF_SEEK_SET) == -1);
    assert(udfread_file_seek(f, (int64_t)size + 1, UDF_SEEK_SET) == -1);
    assert(udfread_file_seek(f, 0, 99) == -1);
    assert(udfread_file_tell(f) == (int64_t)size);
    puts("API case5 seek-and-boundary-errors PASS");

    unsigned char block[UDF_BLOCK_SIZE];
    assert(udfread_file_lba(f, 0) > 0);
    assert(udfread_read_blocks(f, block, 0, 1, 0) == 1);
    assert(memcmp(block, expected, sizeof(block)) == 0);
    UDFFILE *n = udfread_file_openat(sub, "nested.txt");
    assert(n != NULL && udfread_file_size(n) == (int64_t)(sizeof(nested) - 1));
    assert(udfread_file_read(n, actual, sizeof(nested)) == (ssize_t)(sizeof(nested) - 1));
    assert(memcmp(actual, nested, sizeof(nested) - 1) == 0);
    assert(udfread_file_read(n, actual, 1) == 0);
    udfread_file_close(n); udfread_file_close(f);
    udfread_closedir(sub); udfread_closedir(root); udfread_close(u);
    free(actual); free(expected);
    puts("API case6 block-and-relative-file-read PASS");
    puts("libudfread API cases 6/6 PASS");
    return 0;
}
LIBUDFREAD_API_EOF

%build
# No Meson feature/default override: upstream requests both shared and static.
CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" meson setup build --prefix=%{_prefix} --libdir=%{_libdir} --wrap-mode=nodownload
meson compile -C build
gcc %{optflags} -UNDEBUG -Ibuild/src api-smoke.c -Lbuild/src -ludfread -o api-smoke
# A regular-file fixture is generated only in target CI, never mounted/burned.
mkdir -p fixture-root/sub
i=0
while [ "$i" -lt 200 ]; do
    printf 'libudfread test payload\n'
    i=$((i+1))
done > fixture-root/payload.txt
printf 'nested UDF contents\n' > fixture-root/sub/nested.txt
genisoimage -quiet -udf -V UDFREAD_TEST -o fixture.udf fixture-root

%install
DESTDIR=%{buildroot} meson install -C build --no-rebuild
install -Dpm0755 api-smoke %{buildroot}%{_libexecdir}/libudfread-tests/api-smoke
install -Dpm0644 api-smoke.c %{buildroot}%{_libexecdir}/libudfread-tests/api-smoke.c
install -Dpm0644 fixture.udf %{buildroot}%{_libexecdir}/libudfread-tests/fixture.udf

%check
# Original Meson test entry point registers zero upstream runtime cases.
meson test -C build --print-errorlogs
test -f build/src/libudfread.a
test -f build/src/libudfread.so.3.0.0
(cd license-notices; sha256sum -c SHA256SUMS)
LD_LIBRARY_PATH="$PWD/build/src" ./api-smoke "$PWD/fixture.udf"
# %check follows install-post stripping: bind the actual packaged driver bytes.
(cd %{buildroot}%{_libexecdir}/libudfread-tests; sha256sum api-smoke api-smoke.c fixture.udf > SHA256SUMS)

%files
%license COPYING license-notices
%doc ChangeLog
%{_includedir}/udfread
%{_libdir}/libudfread.so*
%{_libdir}/libudfread.a
%{_libdir}/pkgconfig/libudfread.pc
%{_libexecdir}/libudfread-tests

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Preserve Meson defaults and all 26 original source/notice files.
- Add six regular-image API regressions and strict installed library bindings.
