#!/bin/bash
set -euo pipefail
run_installed_tests() {
    root=$1
    temp=$(mktemp -d)
    tar -xzf "$root/usr/share/cgreen/qa/cgreen-1.7.0.tar.gz" -C "$temp"
    source="$temp/cgreen-feeb85ed48d163f6b7b0011a6d8e6043951541e4"
    mkdir "$temp/harness"
    cat > "$temp/harness/CMakeLists.txt" <<'CMAKE'
cmake_minimum_required(VERSION 3.13)
project(cgreen_installed_tests C CXX)
include(CheckIncludeFile)
find_package(Threads REQUIRED)
find_package(LibXml2 REQUIRED)
enable_testing()
set(CGREEN_WITH_XML ON)
set(CGREEN_WITH_LIBXML2 ON)
set(CGREEN_WITH_STATIC_LIBRARY OFF)
set(CGREEN_SHARED_LIBRARY installed_cgreen)
add_library(installed_cgreen SHARED IMPORTED)
set_target_properties(installed_cgreen PROPERTIES IMPORTED_LOCATION "${INSTALL_ROOT}/usr/lib64/libcgreen.so.1.7.0")
set(CGREEN_PUBLIC_INCLUDE_DIRS "${INSTALL_ROOT}/usr/include" "${UPSTREAM}" "${UPSTREAM}/src")
set(CMAKE_MODULE_PATH "${UPSTREAM}/cmake/Modules")
include(DefineCompilerFlags)
include(MacroAddTest)
include(MacroAddValgrindTest)
macro(macro_add_unit_test name sources)
    add_executable(${name} ${sources})
    target_link_libraries(${name} ${ARGN})
    macro_add_test(NAME ${name} COMMAND ${CMAKE_CURRENT_BINARY_DIR}/${name})
endmacro()
add_subdirectory("${UPSTREAM}/tests" "${CMAKE_BINARY_DIR}/tests")
CMAKE
    cmake -S "$temp/harness" -B "$temp/build" -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_FLAGS='-O2 -g -UNDEBUG' -DCMAKE_CXX_FLAGS='-O2 -g -UNDEBUG' -DINSTALL_ROOT="$root" -DUPSTREAM="$source"
    cmake --build "$temp/build" --parallel 2
    mkdir "$temp/build/tools"
    ln -s "$root/usr/bin/cgreen-runner" "$temp/build/tools/cgreen-runner"
    PATH="$root/usr/bin:$PATH" LD_LIBRARY_PATH="$root/usr/lib64" ctest --test-dir "$temp/build" --output-on-failure --no-tests=error -V
    rm -rf -- "$temp"
    echo 'PASS cgreen unchanged tests-directory suite linked to installed shared library and runner'
}
run_installed_tests ''
