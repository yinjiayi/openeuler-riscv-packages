# SPDX-License-Identifier: Apache-2.0
# Only headers, CMake metadata and source fixtures are installed, not ELF.
# Keep every default executable build/test but omit an empty debug subpackage.
%global debug_package %{nil}

Name:           libdivide
Version:        5.4.0
Release:        1%{?dist}
Summary:        Header-only C and C++ integer division library
License:        (BSL-1.0 OR Zlib) AND CC0-1.0
URL:            https://libdivide.com
Source0:        https://codeload.github.com/ridiculousfish/libdivide/tar.gz/ea0fb1ad79a116cd561595c930bcaf33147b3e6c#/libdivide-5.4.0.tar.gz
Source1:        https://raw.githubusercontent.com/spdx/license-list-data/d46e94e2c78ceede1cfc63cfa0396472d2798d4c/text/CC0-1.0.txt#/CC0-1.0.txt
BuildRequires:  gcc gcc-c++ cmake make glibc-devel libstdc++-devel
BuildRequires:  bash coreutils binutils rpm gzip tar grep gawk sed findutils diffutils
Requires:       gcc gcc-c++ cmake make glibc-devel libstdc++-devel bash coreutils grep

%description
Header-only integer division for C and C++, installed CMake import targets,
constant-divider helper headers and unchanged original test inputs.
Arithmetic validation is distinct from native hardware performance validation.

%prep
%setup -q -n libdivide-ea0fb1ad79a116cd561595c930bcaf33147b3e6c
cp %{SOURCE1} CC0-1.0.txt
cat > run-original-tests.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
root=${1:-}
test -z "$root" || test "${root:0:1}" = /
root=${root%/}
inputs="$root/usr/share/libdivide/tests"
cd "$inputs"
sha256sum -c SHA256SUMS
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
# Sources use only RPM-installed implementation headers.
test ! -e libdivide.h
g++ -std=c++11 -O3 -UNDEBUG -Wall -Wextra -pedantic -Werror -pthread -I"$root/usr/include" tester.cpp -o "$work/tester"
gcc -std=gnu99 -O3 -UNDEBUG -Wall -Wextra -pedantic -Werror -I"$root/usr/include" test_c99.c -o "$work/test_c99"
gcc -std=gnu99 -O3 -UNDEBUG -Wall -Wextra -pedantic -Werror test_divlu.c divlu.c -o "$work/test_divlu"
g++ -std=c++11 -O3 -UNDEBUG -Wall -Wextra -pedantic -Werror -I"$root/usr/include" benchmark_branchfree.cpp -o "$work/benchmark_branchfree"
for program in tester test_c99 test_divlu benchmark_branchfree; do
    "$work/$program" > "$work/$program.log" 2>&1
    cat "$work/$program.log"
    if grep -E 'Division fail:|^Error:|^FAIL' "$work/$program.log"; then
        printf 'ERROR original program reported a failure: %s\n' "$program" >&2
        exit 1
    fi
    case "$program" in
        tester|benchmark_branchfree) grep -F 'All tests passed successfully!' "$work/$program.log" ;;
    esac
    printf 'PASS original installed program=%s unmodified-default-arguments\n' "$program"
done
cmake -S consumer -B "$work/consumer" -DCMAKE_BUILD_TYPE=Release -Dlibdivide_DIR="$root/usr/lib64/cmake/libdivide"
cmake --build "$work/consumer" --parallel 1
"$work/consumer/consumer"
printf 'PASS downstream installed CMake target version=5.4.0\n'
printf 'BOUNDARY arithmetic-only; QEMU timings are not native performance evidence\n'
SH
mkdir consumer
cat > consumer/CMakeLists.txt <<'CMAKE'
cmake_minimum_required(VERSION 3.5)
project(installed_libdivide CXX)
find_package(libdivide 5.4.0 EXACT REQUIRED CONFIG)
add_executable(consumer consumer.cpp)
target_link_libraries(consumer PRIVATE libdivide::libdivide)
target_compile_options(consumer PRIVATE -Wall -Wextra -pedantic -Werror -UNDEBUG)
CMAKE
cat > consumer/consumer.cpp <<'CPP'
// SPDX-License-Identifier: Apache-2.0
#include <cassert>
#include <cstdint>
#include <libdivide.h>
#include <constant_fast_div.h>
#include <constant_fast_div.hpp>
int main() {
    const libdivide::divider<std::uint64_t> d(7);
    for (std::uint64_t n = 0; n < 4096; ++n) {
        assert(n / d == n / 7);
        assert((libdivide::fast_divide<std::uint16_t, 7>(static_cast<std::uint16_t>(n)) == n / 7));
        assert(FAST_DIV16U(static_cast<std::uint16_t>(n), 7) == n / 7);
    }
    return 0;
}
CPP

%build
# Keep Release optimization, default targets, AUTO probes and diagnostics.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=lib64 -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS="%{optflags}" -DCMAKE_CXX_FLAGS="%{optflags}" -DCMAKE_C_FLAGS_RELEASE="-O3 -UNDEBUG" -DCMAKE_CXX_FLAGS_RELEASE="-O3 -UNDEBUG"
cmake --build build --parallel %{?_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -m 0644 constant_fast_div.h constant_fast_div.hpp s16_ldparams.h s16_ldparams.hpp u16_ldparams.h u16_ldparams.hpp %{buildroot}%{_includedir}/
install -d %{buildroot}%{_datadir}/libdivide/tests/consumer
install -m 0644 test/tester.cpp test/DivideTest.h test/outputs.h test/type_mappings.h test/avr_type_helpers.h test/test_c99.c test/test_divlu.c test/benchmark_branchfree.cpp doc/divlu.c %{buildroot}%{_datadir}/libdivide/tests/
install -m 0644 consumer/CMakeLists.txt consumer/consumer.cpp %{buildroot}%{_datadir}/libdivide/tests/consumer/
install -m 0755 run-original-tests.sh %{buildroot}%{_datadir}/libdivide/tests/
(cd %{buildroot}%{_datadir}/libdivide/tests; sha256sum *.c *.cpp *.h consumer/* > SHA256SUMS)

%check
# Complete original Release CTest, including the finite benchmark checksum.
# The unregistered benchmark/benchmark_divlu infinite loops are built only.
ctest --test-dir build -N > registered-tests.log
cat registered-tests.log
grep -E '^Total Tests: 8$' registered-tests.log
ctest --test-dir build --verbose --parallel 1 > original-ctest.log 2>&1
cat original-ctest.log
grep -F '100% tests passed, 0 tests failed out of 8' original-ctest.log
# Original C99 failures print without nonzero status; additionally reject them.
if grep -F 'Division fail:' original-ctest.log; then exit 1; fi
bash %{buildroot}%{_datadir}/libdivide/tests/run-original-tests.sh "%{buildroot}"

%files
%license LICENSE.txt CC0-1.0.txt doc/divlu.c
%doc README.md
%{_includedir}/libdivide.h
%{_includedir}/constant_fast_div.h
%{_includedir}/constant_fast_div.hpp
%{_includedir}/s16_ldparams.h
%{_includedir}/s16_ldparams.hpp
%{_includedir}/u16_ldparams.h
%{_includedir}/u16_ldparams.hpp
%{_libdir}/cmake/libdivide/
%{_datadir}/libdivide/

%changelog
* Fri Oct 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4.0-1
- Pin official source and complete legal texts; preserve all default tests.
- Verify original arithmetic programs against staged and installed headers.
