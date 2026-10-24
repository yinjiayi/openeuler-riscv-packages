# SPDX-License-Identifier: Apache-2.0
Name:           libspatialindex
Version:        2.1.0
Release:        1%{?dist}
Summary:        Spatial indexing library with C and C++ interfaces
License:        MIT AND BSD-3-Clause AND FSFULLR AND Martin-Birgmeier AND ISC
URL:            https://libspatialindex.github.io
Source0:        libspatialindex-2.1.0.tar.gz
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
libspatialindex provides R*-tree, MVR-tree and TPR-tree spatial indexing with
C and C++ interfaces. This package preserves the upstream shared-library and
integrated-test defaults and includes an installed functional API check.

%package devel
Summary:        Development files for libspatialindex
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, shared-library link names, pkg-config and CMake consumer metadata.

%prep
%autosetup -n libspatialindex-175b56a9541e76982d13dbbf0c9b8f0b8d752619 -p1
# Preserve every original member before any generation. A .notice suffix also
# prevents basename-matching build macros from replacing copied helpers.
mkdir license-notices
find . -path ./license-notices -prune -o -type f -print | while IFS= read -r notice_file; do
    notice_file=${notice_file#./}
    mkdir -p "license-notices/$(dirname "$notice_file")"
    cp -p "$notice_file" "license-notices/$notice_file.notice"
done
test "$(find license-notices -type f | wc -l)" -eq 325
(cd license-notices; find . -type f -print | LC_ALL=C sort | while IFS= read -r notice_file; do sha256sum "$notice_file"; done) > original-source.sha256
mv original-source.sha256 license-notices/SHA256SUMS
find license-notices -type f -exec chmod 0644 {} +
cat > api-smoke.cc <<'API_EOF'
/* SPDX-License-Identifier: ISC
 * Copyright (c) 2026 openEuler RISC-V package contributors
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
#include <spatialindex/SpatialIndex.h>
#include <spatialindex/capi/sidx_api.h>
#include <cassert>
#include <cstdio>
#include <cstring>
int main() {
    char *version = SIDX_Version();
    assert(version && std::strcmp(version, "2.1.0") == 0);
    Index_Free(version);
    std::puts("api version: PASS");
    double coordinates[2] = {1.25, 2.5};
    SpatialIndex::Point point(coordinates, 2);
    assert(point.getDimension() == 2 && point.getCoordinate(0) == 1.25);
    std::puts("api C++ point: PASS");
    IndexPropertyH props = IndexProperty_Create();
    assert(props);
    assert(IndexProperty_SetIndexType(props, RT_RTree) == RT_None);
    assert(IndexProperty_SetIndexStorage(props, RT_Memory) == RT_None);
    assert(IndexProperty_SetDimension(props, 2) == RT_None);
    IndexH index = Index_Create(props);
    IndexProperty_Destroy(props);
    assert(index && Index_IsValid(index));
    std::puts("api memory index: PASS");
    double lower[2] = {1.0, 2.0}, upper[2] = {2.0, 3.0};
    const uint8_t data[] = {0, 17, 255};
    assert(Index_InsertData(index, 42, lower, upper, 2, data, sizeof data) == RT_None);
    uint64_t count = 99;
    assert(Index_Intersects_count(index, lower, upper, 2, &count) == RT_None && count == 1);
    int64_t *ids = nullptr;
    count = 99;
    assert(Index_Intersects_id(index, lower, upper, 2, &ids, &count) == RT_None);
    assert(ids && count == 1 && ids[0] == 42);
    Index_Free(ids);
    std::puts("api insert and intersection: PASS");
    double outside_lower[2] = {10.0, 10.0}, outside_upper[2] = {11.0, 11.0};
    assert(Index_Intersects_count(index, outside_lower, outside_upper, 2, &count) == RT_None && count == 0);
    std::puts("api disjoint query: PASS");
    assert(Index_DeleteData(index, 42, lower, upper, 2) == RT_None);
    assert(Index_Intersects_count(index, lower, upper, 2, &count) == RT_None && count == 0);
    assert(Index_IsValid(index));
    Index_Destroy(index);
    std::puts("api delete: PASS");
}
API_EOF
sed -n '1,/^ \*\//p' api-smoke.cc > PACKAGING-COPYING

%build
# Use a relative libdir: upstream's export(FILE ...) also uses this variable.
# Do not override BUILD_TESTING/BUILD_SHARED_LIBS, shrink fixtures or add filters.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_C_FLAGS="%{optflags}" -DCMAKE_CXX_FLAGS="%{optflags}" \
    -DCMAKE_EXE_LINKER_FLAGS="%{?build_ldflags}" -DCMAKE_SHARED_LINKER_FLAGS="%{?build_ldflags}"
cmake --build build --parallel %{?_smp_build_ncpus}
g++ %{optflags} -UNDEBUG -Iinclude api-smoke.cc -Lbuild/src \
    -Wl,-rpath-link,"$PWD/build/src" %{?build_ldflags} -lspatialindex_c -lspatialindex -o api-smoke

%install
DESTDIR=%{buildroot} cmake --install build
install -D -m0755 api-smoke %{buildroot}%{_libexecdir}/libspatialindex-tests/api-smoke

%check
(cd license-notices; sha256sum -c SHA256SUMS)
test "$(wc -l < license-notices/SHA256SUMS)" -eq 325
grep -Fx 'BUILD_TESTING:BOOL=ON' build/CMakeCache.txt
grep -Fx 'BUILD_SHARED_LIBS:BOOL=ON' build/CMakeCache.txt
# This is the complete unmodified upstream CTest set, including the original
# million-entry RTree fixture and bundled GTest integration, with no filter.
ctest --test-dir build --verbose --output-on-failure
LD_LIBRARY_PATH="$PWD/build/src${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" ./api-smoke
# RPM's install-post stripping precedes check; bind those installed bytes.
(cd %{buildroot}%{_libexecdir}/libspatialindex-tests; sha256sum api-smoke > SHA256SUMS)

%files
%license COPYING PACKAGING-COPYING license-notices
%doc README.rst NEWS AUTHORS
%{_libdir}/libspatialindex.so.8*
%{_libdir}/libspatialindex_c.so.8*
%{_libexecdir}/libspatialindex-tests/

%files devel
%{_includedir}/spatialindex/
%{_libdir}/libspatialindex.so
%{_libdir}/libspatialindex_c.so
%{_libdir}/pkgconfig/libspatialindex.pc
%{_libdir}/cmake/libspatialindex/

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Pin official stable source; preserve all notices, defaults and original tests.
