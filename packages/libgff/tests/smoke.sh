#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
unset LD_LIBRARY_PATH
rpm -q libgff libgff-devel
rpm -V libgff libgff-devel
test -s /usr/share/licenses/libgff/BoostLicense.txt
test "$(rpm -qf --qf '%{NAME}' /usr/libexec/libgff/TestGFFParse)" = libgff
test -x /usr/libexec/libgff/TestGFFParse
test "$(rpm -qf --qf '%{NAME}' /usr/lib64/libgff.a)" = libgff-devel
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
cd /usr/share/libgff/tests
sha256sum -c SHA256SUMS
bash check-parser.sh /usr/libexec/libgff/TestGFFParse "$work/original-installed-results"
g++ -O2 -UNDEBUG -std=c++14 TestGFFParse.cpp /usr/lib64/libgff.a -o "$work/parser"
bash check-parser.sh "$work/parser" "$work/results"
mkdir "$work/consumer"
printf '%s\n' 'cmake_minimum_required(VERSION 3.12)' 'project(installed_gff CXX)' \
  'find_package(libgff 2.0 REQUIRED CONFIG)' \
  'add_executable(parser /usr/share/libgff/tests/TestGFFParse.cpp)' \
  'target_compile_features(parser PRIVATE cxx_std_14)' \
  'target_include_directories(parser PRIVATE ${LIB_GFF_INCLUDE_DIR})' \
  'target_link_libraries(parser PRIVATE ${LIB_GFF_STATIC_LIBRARY})' > "$work/consumer/CMakeLists.txt"
cmake -S "$work/consumer" -B "$work/build"
cmake --build "$work/build" --parallel 1
bash check-parser.sh "$work/build/parser" "$work/cmake-results"
