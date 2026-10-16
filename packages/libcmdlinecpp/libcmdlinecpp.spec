# SPDX-License-Identifier: Apache-2.0
Name:           libcmdlinecpp
Version:        1.0.0
Release:        1%{?dist}
Summary:        C++11 command-line argument parser
License:        LGPL-3.0-or-later
URL:            https://github.com/nullptrT/libcmdlinecpp
Source0:        libcmdlinecpp-1.0.0.tar.gz
Source1:        COPYING.GPL3
Patch0:         patches/0001-export-valid-static-library-metadata.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconf
Requires:       gcc-c++
Requires:       cmake
Requires:       make
Requires:       pkgconf

%description
A C++11 parser for positional arguments, options and actions. This package
retains upstream's default static library and headers, CMake/pkg-config
metadata and all four original example programs and their source.

%prep
%setup -q -n libcmdlinecpp-db5417e4853aa5d0a07b8e8c1fb697375dde1188
%patch0 -p1
cp -p %{SOURCE1} COPYING.GPL3

%build
%cmake_conf -DCMDLINECPP_INSTALL_LIBS=ON -DBUILD_CMDLINECPP_TESTS=ON \
  -DCMDLINECPP_LIB_INSTALL_DIR=%{_libdir} \
  -DCMDLINECPP_HEADER_INSTALL_DIR=%{_includedir}/libcmdlinecpp
%cmake_build

%install
%cmake_install
install -d %{buildroot}%{_libexecdir}/libcmdlinecpp \
  %{buildroot}%{_datadir}/libcmdlinecpp/tests/examples
for name in cmdlinecpp_test cmdlinecpp_test2 cmdlinecpp_test_action cmdlinecpp_test_last_positional_list; do
  install -m 0755 %{_vpath_builddir}/src/examples/$name %{buildroot}%{_libexecdir}/libcmdlinecpp/
done
install -m 0644 src/examples/*.cpp %{buildroot}%{_datadir}/libcmdlinecpp/tests/examples/
sha256sum src/examples/*.cpp | sed 's@  src/examples/@  examples/@' > %{buildroot}%{_datadir}/libcmdlinecpp/tests/SHA256SUMS
sha256sum src/*.hpp | sed 's@  src/@  @' > %{buildroot}%{_datadir}/libcmdlinecpp/tests/HEADERS.SHA256SUMS
cat > %{buildroot}%{_datadir}/libcmdlinecpp/tests/run-checks.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
base="$root/usr/share/libcmdlinecpp/tests"
prefix="$root/usr"
test -f "$prefix/lib64/libcmdlinecpp.a"
(cd "$base"; sha256sum -c SHA256SUMS)
(cd "$prefix/include/libcmdlinecpp"; sha256sum -c "$base/HEADERS.SHA256SUMS")
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
for source in "$base"/examples/*.cpp; do
  name=$(basename "$source" .cpp)
  g++ -std=c++11 -DLIBCMDLINECPP_VERSION='"1.0.0"' -I"$prefix/include/libcmdlinecpp" \
    "$source" "$prefix/lib64/libcmdlinecpp.a" -o "$work/$name"
  "$work/$name" --help fixture > "$work/$name.help" 2>&1
  grep -F 'PATH' "$work/$name.help"
  status=0
  "$work/$name" > "$work/$name.empty" 2>&1 || status=$?
  test "$status" -eq 1
  grep -F 'Not all positional arguments' "$work/$name.empty"
done
"$work/main" -n 3 fixture
"$work/main_action" read fixture > "$work/action"
grep -Fx "Selected action: 'read'." "$work/action"
"$work/main_last_positional" read fixture alpha beta > "$work/list"
grep -Fx 'alpha' "$work/list"
grep -Fx 'beta' "$work/list"
cat > "$work/consumer.cpp" <<'CPP'
#include <libcmdlinecpp/cmdline.hpp>
#include <string>
int main() {
    cmdline << cmdlinecpp::Option("PATH", "input");
    cmdline << cmdlinecpp::Option("iterations", "n", "count", cmdlinecpp::Data::Type::Int);
    char a0[]="check", a1[]="-n", a2[]="3", a3[]="fixture";
    char* args[]={a0,a1,a2,a3};
    if (!cmdline.parse(4,args)) return 1;
    int count=0; cmdline >> cmdlinecpp::Data("iterations") >> count;
    return cmdline["PATH"]=="fixture" && count==3 && cmdline.is_specified("iterations") ? 0 : 2;
}
CPP
PKG_CONFIG_PATH="$prefix/lib64/pkgconfig" PKG_CONFIG_SYSROOT_DIR="$root" pkg-config --exists --exact-version=1.0.0 libcmdlinecpp
# For a staged root the .pc absolute library filename needs the same root;
# compile against that physical archive and independently verify its metadata.
grep -Fx 'Libs: ${libdir}/libcmdlinecpp.a' "$prefix/lib64/pkgconfig/libcmdlinecpp.pc"
g++ -std=c++11 -I"$prefix/include" "$work/consumer.cpp" "$prefix/lib64/libcmdlinecpp.a" -o "$work/consumer"
"$work/consumer"
cat > "$work/CMakeLists.txt" <<'CMAKE'
cmake_minimum_required(VERSION 3.12)
project(libcmdlinecpp_consumer LANGUAGES CXX)
find_package(LibCmdLineCPP CONFIG REQUIRED)
if(NOT LIBCMDLINECPP_VERSION_STRING STREQUAL "1.0.0")
  message(FATAL_ERROR "Unexpected installed library version")
endif()
add_executable(consumer consumer.cpp)
target_include_directories(consumer PRIVATE ${LIBCMDLINECPP_INCLUDE_DIR})
target_link_libraries(consumer PRIVATE ${LIBCMDLINECPP_LIBRARY_STATIC})
target_compile_features(consumer PRIVATE cxx_std_11)
CMAKE
cmake -S "$work" -B "$work/build" -DCMAKE_PREFIX_PATH="$prefix" -DCMAKE_FIND_ROOT_PATH="$root" \
  -DLibCmdLineCPP_DIR="$prefix/lib64/cmake/LibCmdLineCPP" \
  -DCMAKE_FIND_ROOT_PATH_MODE_LIBRARY=ONLY -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=ONLY
cmake --build "$work/build" --verbose
"$work/build/consumer"
echo 'PASS downstream examples=4 help-and-rejection=8 functional-vectors=3 consumers=2 skips=0'
SH
chmod 0755 %{buildroot}%{_datadir}/libcmdlinecpp/tests/run-checks.sh

%check
# Upstream registers no CTest suite or assertive test target. Build all four
# unchanged original examples; downstream checks are labelled as such.
for name in cmdlinecpp_test cmdlinecpp_test2 cmdlinecpp_test_action cmdlinecpp_test_last_positional_list; do
  %{_vpath_builddir}/src/examples/$name --help fixture
done
bash %{buildroot}%{_datadir}/libcmdlinecpp/tests/run-checks.sh %{buildroot}

%files
%license LICENSE.txt COPYING.GPL3
%doc README.md CHANGELOG.md
%{_includedir}/libcmdlinecpp/
%{_libdir}/libcmdlinecpp.a
%{_libdir}/pkgconfig/libcmdlinecpp.pc
%{_libdir}/cmake/LibCmdLineCPP/
%{_libexecdir}/libcmdlinecpp/
%{_datadir}/libcmdlinecpp/

%changelog
* Sat Oct 17 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Pin official stable source, retain default static library and all original examples.
- Export correct static consumer/version metadata and include full LGPL3/GPL3 texts.
- Add explicitly downstream staged/installed example and semantic consumer checks.
