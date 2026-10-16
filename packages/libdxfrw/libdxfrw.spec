# SPDX-License-Identifier: Apache-2.0
%global upstream_commit 945f2161a13ee521f66f9c52dcfff998e8ccae99
Name:           libdxfrw
Version:        1.0.1
Release:        1%{?dist}
Summary:        C++ library and converter for ASCII and binary DXF drawings
License:        GPL-2.0-or-later AND LicenseRef-Rockliff-1991
URL:            https://github.com/LibreCAD/libdxfrw
Source0:        libdxfrw-1.0.1.tar.gz
Source1:        COPYING.GPL3
Patch0:         0001-correct-installed-pkgconfig-paths.patch
Patch1:         0002-preserve-entity-dispatch-handoff.patch
Patch2:         0003-preserve-pkgconfig-template-variables.patch
Patch3:         0004-write-header-booleans-at-binary-width.patch
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  binutils
BuildRequires:  rpm
BuildRequires:  gzip
BuildRequires:  tar
BuildRequires:  grep
BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  findutils
BuildRequires:  diffutils
BuildRequires:  patch

%description
Library for reading DWG and reading/writing ASCII and binary DXF, including
the original dwg2dxf converter. Validation covers downstream DXF round trips,
not the full DWG format or a nonexistent upstream semantic test suite.

%package devel
Summary:        Headers, static library and development metadata for libdxfrw
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc-c++
Requires:       cmake
Requires:       make
Requires:       pkgconf
Requires:       bash
Requires:       coreutils
Requires:       binutils
Requires:       rpm
Provides:       %{name}-static = %{version}-%{release}

%description devel
Installed public headers, shared-library linker symlink, original default
static library, pkg-config and CMake exports, and downstream DXF contract
fixtures using the unchanged upstream converter interface implementation.

%prep
%autosetup -n libdxfrw-%{upstream_commit} -p1
cp -p %{SOURCE1} COPYING.GPL3
mkdir contract
cp -p dwg2dxf/dx_iface.cpp dwg2dxf/dx_iface.h dwg2dxf/dx_data.h contract/
cat > contract/check-dxf.cpp <<'CPP'
// SPDX-License-Identifier: Apache-2.0
// Downstream semantic fixture; dx_iface implementation is unmodified upstream.
#include <cmath>
#include <iostream>
#include "dx_iface.h"
static bool eq(double a, double b) { return std::fabs(a-b) < 1e-9; }
static bool coord(const DRW_Coord& p, double x, double y, double z) {
    return eq(p.x,x) && eq(p.y,y) && eq(p.z,z);
}
int main(int argc, char** argv) {
    if (argc != 2) return 2;
    dx_data data;
    dx_iface iface;
    if (!iface.fileImport(argv[1], &data)) return 3;
    if (data.mBlock->ent.size() != 3) return 4;
    unsigned lines=0, circles=0, points=0;
    for (const auto* entity : data.mBlock->ent) {
        if (entity->layer != "0") return 5;
        if (entity->eType == DRW::LINE) {
            const auto* line = static_cast<const DRW_Line*>(entity);
            if (!coord(line->basePoint,1,2,0) || !coord(line->secPoint,4,6,0)) return 6;
            ++lines;
        } else if (entity->eType == DRW::CIRCLE) {
            const auto* circle = static_cast<const DRW_Circle*>(entity);
            if (!coord(circle->basePoint,8,9,0) || !eq(circle->radious,2.5)) return 7;
            ++circles;
        } else if (entity->eType == DRW::POINT) {
            const auto* point = static_cast<const DRW_Point*>(entity);
            if (!coord(point->basePoint,-3,7,0)) return 8;
            ++points;
        } else return 9;
    }
    if (lines != 1 || circles != 1 || points != 1) return 10;
    std::cout << "PASS downstream DXF entities=3 coordinates=verified layer=0\n";
    return 0;
}
CPP
cat > contract/fixture.dxf <<'DXF'
0
SECTION
2
HEADER
9
$ACADVER
1
AC1015
0
ENDSEC
0
SECTION
2
ENTITIES
0
LINE
8
0
10
1.0
20
2.0
30
0.0
11
4.0
21
6.0
31
0.0
0
CIRCLE
8
0
10
8.0
20
9.0
30
0.0
40
2.5
0
POINT
8
0
10
-3.0
20
7.0
30
0.0
0
ENDSEC
0
EOF
DXF
cat > contract/CMakeLists.txt <<'CMAKE'
# SPDX-License-Identifier: Apache-2.0
cmake_minimum_required(VERSION 3.5)
project(dxfrw_installed_contract LANGUAGES CXX)
find_package(libdxfrw 1.0.1 CONFIG REQUIRED)
add_executable(check-dxf check-dxf.cpp dx_iface.cpp)
target_compile_features(check-dxf PRIVATE cxx_std_11)
target_compile_options(check-dxf PRIVATE -UNDEBUG)
target_link_libraries(check-dxf PRIVATE libdxfrw::libdxfrw)
CMAKE
cat > contract/run-contract.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -Eeuxo pipefail
# Fixture-only commands contain no credentials or external input. Preserve the
# failing command, line and status in the captured RPM log, including functions.
trap 'rc=$?; printf "FAIL contract line=%s status=%s command=%s\n" "$LINENO" "$rc" "$BASH_COMMAND" >&2' ERR
test "$#" -le 1
root=${1:-/}
prefix="${root%/}/usr"
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
cleanup() {
    rc=$?
    if test "$rc" -eq 0; then rm -rf -- "$work"; else printf 'FAIL evidence retained: %s\n' "$work" >&2; fi
    exit "$rc"
}
trap cleanup EXIT
cd "$self"
sha256sum -c SHA256SUMS
export LD_LIBRARY_PATH="$prefix/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PKG_CONFIG_LIBDIR="$prefix/lib64/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="${root%/}"
test "$(pkg-config --modversion libdxfrw)" = 1.0.1
pkg-config --validate libdxfrw
read -r -a pc_includes <<< "$(pkg-config --cflags-only-I libdxfrw)"
test "${#pc_includes[@]}" -eq 1
test "${pc_includes[0]}" = "-I$prefix/include/libdxfrw"
read -r -a pc_libraries <<< "$(pkg-config --libs libdxfrw)"
test "${#pc_libraries[@]}" -eq 2
test "${pc_libraries[0]}" = "-L$prefix/lib64"
test "${pc_libraries[1]}" = -ldxfrw
cp check-dxf.cpp dx_iface.cpp dx_iface.h dx_data.h CMakeLists.txt fixture.dxf "$work/"
cd "$work"
c++ -std=c++11 -O2 -UNDEBUG $(pkg-config --cflags libdxfrw) check-dxf.cpp dx_iface.cpp $(pkg-config --libs libdxfrw) -o pc-check
./pc-check fixture.dxf
"$prefix/bin/dwg2dxf" fixture.dxf -b -v2000 binary.dxf
printf 'AutoCAD Binary DXF\r\n\032\000' > magic.expected
head -c 22 binary.dxf > magic.actual
cmp magic.expected magic.actual
./pc-check binary.dxf
"$prefix/bin/dwg2dxf" binary.dxf -v2000 ascii.dxf
./pc-check ascii.dxf
cmake -S . -B cmake-consumer -Dlibdxfrw_DIR="$prefix/lib64/cmake/libdxfrw" -DCMAKE_BUILD_TYPE=Release
cmake --build cmake-consumer --verbose --parallel 1
./cmake-consumer/check-dxf ascii.dxf
c++ -std=c++11 -O2 -UNDEBUG $(pkg-config --cflags libdxfrw) check-dxf.cpp dx_iface.cpp "$prefix/lib64/libdxfrw.a" -o static-check
./static-check binary.dxf
if "$prefix/bin/dwg2dxf" missing.dxf -v2000 invalid.dxf; then echo 'FAIL missing input accepted' >&2; exit 1; fi
test ! -e invalid.dxf
if "$prefix/bin/dwg2dxf"; then echo 'FAIL invalid CLI accepted' >&2; exit 1; fi
echo 'PASS downstream DXF replays=5 original-semantic-tests=0 CLI-negative=2'
SH
chmod 0755 contract/run-contract.sh
(cd contract && sha256sum dx_iface.cpp dx_iface.h dx_data.h check-dxf.cpp fixture.dxf CMakeLists.txt > SHA256SUMS)

%build
# Preserve the original static default and converter, then add the shared ABI.
# Set includedir before upstream constructs LIBDXFRW_INSTALL_INCLUDEDIR.
cmake -S . -B build-static -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} -DCMAKE_INSTALL_INCLUDEDIR=include \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -g -UNDEBUG" \
    -DCMAKE_EXE_LINKER_FLAGS="%{?build_ldflags}"
cmake --build build-static --verbose --parallel 2
cmake -S . -B build-shared -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_INSTALL_INCLUDEDIR=include -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="%{optflags} -g -UNDEBUG" \
    -DCMAKE_EXE_LINKER_FLAGS="%{?build_ldflags}" -DCMAKE_SHARED_LINKER_FLAGS="%{?build_ldflags}"
cmake --build build-shared --verbose --parallel 2

%install
DESTDIR=%{buildroot} cmake --install build-shared
install -m 0644 build-static/libdxfrw.a %{buildroot}%{_libdir}/libdxfrw.a
install -d %{buildroot}%{_datadir}/libdxfrw/tests
cp -p contract/* %{buildroot}%{_datadir}/libdxfrw/tests/

%check
# This release registers no upstream CTest/Automake semantic tests.
# Exercise the unchanged original CLI from BOTH default-static and shared builds.
mkdir build-contract
build-static/dwg2dxf/dwg2dxf contract/fixture.dxf -v2000 build-contract/static.dxf
LD_LIBRARY_PATH="$PWD/build-shared" build-shared/dwg2dxf/dwg2dxf \
    contract/fixture.dxf -b -v2000 build-contract/shared.dxf
bash %{buildroot}%{_datadir}/libdxfrw/tests/run-contract.sh %{buildroot}
# Reuse the installed-header consumer to check the default CLI's outputs too.
g++ -std=c++11 -O2 -UNDEBUG -I%{buildroot}%{_includedir}/libdxfrw \
    contract/check-dxf.cpp contract/dx_iface.cpp %{buildroot}%{_libdir}/libdxfrw.a -o build-contract/check
build-contract/check build-contract/static.dxf
build-contract/check build-contract/shared.dxf

%files
%license COPYING COPYING.GPL3 src/intern/rscodec.cpp install-sh ar-lib config.guess config.sub depcomp missing ltmain.sh
%doc README AUTHORS ChangeLog
%{_libdir}/libdxfrw.so.1*
%{_bindir}/dwg2dxf
%{_mandir}/man1/dwg2dxf.1*

%files devel
%{_includedir}/libdxfrw/
%{_libdir}/libdxfrw.so
%{_libdir}/libdxfrw.a
%{_libdir}/pkgconfig/libdxfrw.pc
%{_libdir}/cmake/libdxfrw/
%{_datadir}/libdxfrw/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Pin official stable source; preserve default static library and converter.
- Add shared ABI and repair installed pkg-config paths without disabling tests.
- Add separately identified installed-header/API/CLI DXF round-trip contracts.
