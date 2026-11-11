# SPDX-License-Identifier: Apache-2.0
# No ELF is shipped: upstream is a header-only INTERFACE library.
%global debug_package %{nil}
Name:           libshrinkwrap
Version:        1.2.0
Release:        1%{?dist}
Summary:        Header-only C++ stream buffers for compression formats
License:        MIT AND BSD-3-Clause
URL:            https://github.com/jonathonl/shrinkwrap
Source0:        https://codeload.github.com/jonathonl/shrinkwrap/tar.gz/eaac292b255b5de45d6546a794ffbd103335bc40#/libshrinkwrap-1.2.0.tar.gz
Source1:        https://raw.githubusercontent.com/facebook/zstd/ebf275912aeb046b9379ec48cfd0e336a542f590/LICENSE#/ZSTD-LICENSE
Source2:        https://raw.githubusercontent.com/facebook/zstd/ebf275912aeb046b9379ec48cfd0e336a542f590/PATENTS#/ZSTD-PATENTS
Patch0:         0001-include-cstdint-for-public-integer-types.patch
BuildArch:      noarch
BuildRequires:  gcc gcc-c++ libstdc++-devel glibc-devel cmake make zlib-devel xz-devel zstd-devel
BuildRequires:  bash coreutils binutils rpm gzip tar grep gawk sed findutils diffutils patch
Requires:       gcc-c++ cmake make zlib-devel xz-devel zstd-devel bash coreutils rpm

%description
Header-only C++ stream buffers and input/output streams for stdio, gzip/BGZF,
XZ and Zstandard. Includes original CMake integration and unchanged test source
with an installed consumer replay wrapper. Not the Java ShrinkWrap project.

%prep
%autosetup -p1 -n shrinkwrap-eaac292b255b5de45d6546a794ffbd103335bc40
cp -p %{SOURCE1} ZSTD-LICENSE
cp -p %{SOURCE2} ZSTD-PATENTS
# The following wrapper is downstream packaging; no upstream file is edited.
cat > run-tests.sh <<'SH'
#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
test "$#" -le 1
root=${1:-/}
prefix=${root%/}/usr
self=$(cd -- "$(dirname -- "$0")" && pwd)
work=$(mktemp -d)
cleanup() { rc=$?; if test "$rc" -eq 0; then rm -r -- "$work"; else printf 'Failed replay retained: %%s\n' "$work" >&2; fi; exit "$rc"; }
trap cleanup EXIT
printf '%%s  %%s\n' 8b8d44f3afdd14ccea3e7ec3dcf0d21da1349580549d138ae6a3fe8bab9f9cc6 "$self/test.cpp" | sha256sum -c -
while read -r hash name; do
    printf '%%s  %%s\n' "$hash" "$prefix/include/shrinkwrap/$name" | sha256sum -c -
done <<'HASHES'
7ba9338e43250685a87565d3b7286a0c308baa341c11920491ef04700f696b56 gz.hpp
f0877892007cfaf0b54e8c629a8cd808765771c1dea4fd4f662c8152b53ba57d istream.hpp
0bea633c7ff176e1ca4acbf5df93edce8cbddd4711599270ac788b13be0be6f0 stdio.hpp
b691c80f122aba1dd159f6dfadd1349d4cb14a837ee0eb3c37dbc903ba09197f xz.hpp
0fddb0946d3b43f4b3830d4968cf812cbdffa097731323f096e60614214d03b0 zstd.hpp
HASHES
cat > "$work/CMakeLists.txt" <<'CMAKE'
cmake_minimum_required(VERSION 3.2)
project(shrinkwrap_installed_replay LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 11)
find_package(shrinkwrap 1.2.0 CONFIG REQUIRED)
get_target_property(found_include shrinkwrap INTERFACE_INCLUDE_DIRECTORIES)
if(NOT found_include STREQUAL "${SW_EXPECTED_PREFIX}/include")
  message(FATAL_ERROR "Wrong imported header prefix: ${found_include}")
endif()
add_executable(replay "${SW_TEST_SOURCE}")
target_link_libraries(replay shrinkwrap)
CMAKE
cmake -S "$work" -B "$work/build" -DCMAKE_PREFIX_PATH="$prefix" -DSW_EXPECTED_PREFIX="$prefix" -DSW_TEST_SOURCE="$self/test.cpp" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS=-UNDEBUG
cmake --build "$work/build" --verbose -j1
cd "$work"
commands=(stdio-iter stdio-seek xz-seek xz-iter gz-iter bgzf-seek bgzf-iter zstd-iter zstd-seek generic-iter generic-seek)
for command in "${commands[@]}"; do
    "$work/build/replay" "$command"
    printf 'PASS original-command %%s\n' "$command"
done
printf 'PASS downstream-installed-replay commands=11 skips=0\n'
SH

%build
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="%{optflags} -UNDEBUG" -DBUILD_TESTS=1
cmake --build build --verbose -j1

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/%{name}/tests
install -pm0644 src/test.cpp %{buildroot}%{_datadir}/%{name}/tests/
install -pm0755 run-tests.sh %{buildroot}%{_datadir}/%{name}/tests/

%check
ctest --test-dir build -N > original-test-list.log
cat original-test-list.log
grep -Fx 'Total Tests: 11' original-test-list.log
ctest --test-dir build --output-on-failure --no-tests=error -j1
bash %{buildroot}%{_datadir}/%{name}/tests/run-tests.sh %{buildroot}

%files
%license LICENSE ZSTD-LICENSE ZSTD-PATENTS
%doc README.md
%{_includedir}/shrinkwrap/
%{_datadir}/shrinkwrap/
%{_datadir}/%{name}/

%changelog
* Fri Oct 16 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.2.0-1
- Preserve original eleven CTest commands and all compression backends.
