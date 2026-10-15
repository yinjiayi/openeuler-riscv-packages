# SPDX-License-Identifier: Apache-2.0
Name:           libfirefly
Version:        3.1.0
Release:        1%{?dist}
Summary:        C++23 header library for fixed-length vector calculations
License:        GPL-3.0-only AND BSD-3-Clause
URL:            https://github.com/tbhaxor/firefly
Source0:        libfirefly-3.1.0.tar.gz
Source1:        googletest-03597a01ee50ed33e9dfd640b249b4be3799d395.tar.gz
BuildRequires:  gcc-c++ >= 14
BuildRequires:  cmake >= 3.24
BuildRequires:  make
BuildRequires:  libstdc++-devel
BuildRequires:  glibc-devel
Requires:       gcc-c++ >= 14
Requires:       coreutils
Requires:       grep
Requires:       bash

%description
C++23 header library for fixed-length vector calculations, with the complete
original unit-test executable and example for installed-header verification.
The RPM version follows upstream tag v3.1.0; upstream's CMake PROJECT_VERSION
still says 3.0.0 and is intentionally not rewritten.

%prep
%setup -q -n firefly-208ef838b3f9290d3d6272b476e0a15f7a6b17fb
tar -xzf %{SOURCE1}
cp googletest-03597a01ee50ed33e9dfd640b249b4be3799d395/LICENSE LICENSE.googletest
# Keep every original source byte and assertion unchanged. The documentation-only
# doxygen-awesome-css gitlink is not referenced by the default CMake build.
test "$(grep -h '^TEST(' tests/vector/*.cpp tests/utilities/*.cpp | wc -l)" -eq 96
if grep -E 'DISABLED_|GTEST_SKIP' tests/vector/*.cpp tests/utilities/*.cpp; then exit 1; fi
mkdir -p downstream
cat > downstream/verify-vector.cpp <<'CPP'
#include <firefly/utilities.hpp>
#include <firefly/vector.hpp>
#include <complex>
#include <iostream>
#include <stdexcept>
#include <type_traits>
int main() {
    unsigned checks = 0;
    auto check = [&checks](bool value) {
        if (!value) throw std::runtime_error("downstream vector check failed");
        ++checks;
    };
    firefly::vector<int, 3> a{1, 2, 3}, b{3, 2, 1};
    auto sum = a + b;
    check(sum[0] == 4); check(sum[1] == 4); check(sum[2] == 4);
    auto shift = a + 10;
    check(shift[0] == 11); check(shift[1] == 12); check(shift[2] == 13);
    auto mixed = a + 0.5;
    static_assert(std::is_same_v<decltype(mixed), firefly::vector<double, 3>>);
    check(mixed[0] == 1.5); check(mixed[2] == 3.5);
    firefly::vector<int, 2> x{1, 2}, y{-2, 1};
    check(firefly::utilities::vector::are_orthogonal(x, y));
    check(firefly::utilities::vector::are_parallel(x, x));
    if (checks != 10) return 1;
    std::cout << "PASS downstream-installed-header checks=10 skips=0\n";
}
CPP
sha256sum headers/firefly/*.hpp tests/vector/*.cpp tests/utilities/*.cpp examples/main.cpp > downstream/SHA256SUMS.original

%build
cmake -S . -B build -G 'Unix Makefiles' \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_CXX_FLAGS="%{optflags} -UNDEBUG" \
  -DFirefly_ENABLE_TESTS=ON \
  -DFirefly_ENABLE_EXAMPLES=ON \
  -DFETCHCONTENT_SOURCE_DIR_GOOGLETEST="$PWD/googletest-03597a01ee50ed33e9dfd640b249b4be3799d395" \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DINSTALL_GTEST=OFF
cmake --build build --parallel %{_smp_build_ncpus}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_libexecdir}/libfirefly %{buildroot}%{_datadir}/libfirefly/tests
install -m 0755 build/tests/FireflyTests %{buildroot}%{_libexecdir}/libfirefly/FireflyTests
install -m 0755 build/examples/example %{buildroot}%{_libexecdir}/libfirefly/firefly-example
install -m 0644 downstream/verify-vector.cpp %{buildroot}%{_datadir}/libfirefly/tests/
cp -a headers tests examples %{buildroot}%{_datadir}/libfirefly/tests/
install -m 0644 downstream/SHA256SUMS.original %{buildroot}%{_datadir}/libfirefly/tests/

%check
sha256sum -c downstream/SHA256SUMS.original
ctest --test-dir build -N > downstream/ctest-list.log
grep -F 'Total Tests: 96' downstream/ctest-list.log
env -u GTEST_FILTER -u GTEST_TOTAL_SHARDS -u GTEST_SHARD_INDEX -u GTEST_REPEAT \
  -u GTEST_SHUFFLE -u GTEST_FAIL_FAST -u GTEST_OUTPUT \
  ctest --test-dir build --output-on-failure
build/examples/example
g++ -std=c++23 %{optflags} -UNDEBUG -I%{buildroot}%{_includedir} \
  downstream/verify-vector.cpp -o downstream/verify-vector
downstream/verify-vector
(cd %{buildroot}%{_datadir}/libfirefly/tests && sha256sum -c SHA256SUMS.original)

%files
%license LICENSE LICENSE.googletest
%doc README.md
%{_includedir}/firefly/
%{_libexecdir}/libfirefly/
%{_datadir}/libfirefly/

%changelog
* Thu Oct 15 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1.0-1
- Pin official release and original GoogleTest dependency, retain all 96 tests,
  examples, source checksums, licenses and installed-header verification offline.
