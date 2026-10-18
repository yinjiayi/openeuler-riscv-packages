# SPDX-License-Identifier: ISC AND BSD-3-Clause AND LicenseRef-Chemeris-2006 AND LicenseRef-Public-Domain
%global upstream_commit feeb85ed48d163f6b7b0011a6d8e6043951541e4
Name:           cgreen
Version:        1.7.0
Release:        1
Summary:        C and C++ unit testing and mocking framework
License:        ISC AND BSD-3-Clause AND LicenseRef-Chemeris-2006 AND LicenseRef-Public-Domain
URL:            https://cgreen-devs.github.io/
Source0:        https://codeload.github.com/cgreen-devs/cgreen/tar.gz/%{upstream_commit}#/cgreen-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.13
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  libxml2-devel
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  perl
BuildRequires:  perl(Cwd)
BuildRequires:  sed
BuildRequires:  diffutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  grep
Requires:       gdb

%description
Cgreen shared library, headers and reflective runner. Both upstream default
XML reporters, the original complete build and CTest suite are preserved.

%package tests
Summary:        Original Cgreen source for installed-library regression tests
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       cmake >= 3.13
Requires:       make
Requires:       binutils
Requires:       libxml2-devel
Requires:       bash
Requires:       coreutils
Requires:       perl
Requires:       perl(Cwd)
Requires:       sed
Requires:       diffutils
Requires:       tar
Requires:       gzip

%description tests
The original tests-directory C and C++ suites and output comparisons replay
against the installed shared library and runner. Additional tools-directory
tests remain part of the complete original build check, not this replay.

%prep
%setup -q -n cgreen-%{upstream_commit}

%build
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_LIBDIR=lib64 -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_C_FLAGS_RELWITHDEBINFO='%{optflags} -UNDEBUG' -DCMAKE_CXX_FLAGS_RELWITHDEBINFO='%{optflags} -UNDEBUG'
grep -qx 'CGREEN_WITH_XML:BOOL=ON' build/CMakeCache.txt
grep -qx 'CGREEN_WITH_LIBXML2:BOOL=ON' build/CMakeCache.txt
grep -qx 'CGREEN_WITH_UNIT_TESTS:BOOL=ON' build/CMakeCache.txt
grep -qx 'CGREEN_WITH_STATIC_LIBRARY:BOOL=OFF' build/CMakeCache.txt
grep -q -- '-DHAVE_LIBXML2_REPORTER=1' build/src/CMakeFiles/cgreen_shared.dir/flags.make
cmake --build build --parallel %{?_smp_build_ncpus}
test -x build/tools/cgreen-runner

%install
DESTDIR=%{buildroot} cmake --install build
mkdir -p %{buildroot}%{_datadir}/cgreen/qa
install -pm0644 %{SOURCE0} %{buildroot}%{_datadir}/cgreen/qa/cgreen-1.7.0.tar.gz

%check
ctest --test-dir build --output-on-failure --no-tests=error -V
run_installed_tests() {
    root=$1
    temp=$(mktemp -d)
    tar -xzf "$root/usr/share/cgreen/qa/cgreen-1.7.0.tar.gz" -C "$temp"
    source="$temp/cgreen-feeb85ed48d163f6b7b0011a6d8e6043951541e4"
    # The original tests also need non-installed internal headers. Verify every
    # installed header before adding the original include tree as a fallback.
    for header in assertions.h boxed_double.h breadcrumb.h cdash_reporter.h cgreen.h cgreen_value.h constraint.h constraint_syntax_helpers.h cpp_assertions.h cpp_constraint.h cute_reporter.h filename.h legacy.h mocks.h string_comparison.h reporter.h runner.h suite.h text_reporter.h unit.h vector.h xml_reporter.h internal/unit_implementation.h internal/mock_table.h internal/mocks_internal.h internal/suite_internal.h internal/assertions_internal.h internal/c_assertions.h internal/cpp_assertions.h internal/cgreen_pipe.h internal/cgreen_time.h internal/runner_platform.h internal/function_macro.h internal/stringify_token.h internal/constraint_syntax_helpers_internal.h; do
        cmp -- "$source/include/cgreen/$header" "$root/usr/include/cgreen/$header"
    done
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
set(CGREEN_PUBLIC_INCLUDE_DIRS "${INSTALL_ROOT}/usr/include" "${UPSTREAM}/include" "${UPSTREAM}" "${UPSTREAM}/src")
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
run_installed_tests '%{buildroot}'

%files
%license LICENSE cmake/Modules/COPYING-CMAKE-SCRIPTS include/cgreen/internal/windows_headers/inttypes.h tools/gopt.c tools/gopt-errors.c tools/gopt.h
%doc README.md
%{_bindir}/cgreen-runner
%{_bindir}/cgreen-debug
%{_includedir}/cgreen
%{_libdir}/libcgreen.so*
%{_libdir}/cmake/cgreen
%{_datadir}/bash-completion/completions/cgreen-runner
%{_datadir}/bash-completion/completions/cgreen-debug
%{_mandir}/man1/cgreen*.1*
%{_mandir}/man5/cgreen.5*

%files tests
%license LICENSE cmake/Modules/COPYING-CMAKE-SCRIPTS include/cgreen/internal/windows_headers/inttypes.h tools/gopt.c tools/gopt-errors.c tools/gopt.h
%{_datadir}/cgreen

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.7.0-1
- Preserve default XML, libxml2, shared library and complete original CTest.
