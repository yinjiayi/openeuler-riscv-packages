# SPDX-License-Identifier: Apache-2.0
%global debug_package %{nil}
%global upstream_commit 161cb3fc4170fa7a3eca9e582cebd27cc4d1fe29
Name:           picosha2
Version:        1.0.1
Release:        1%{?dist}
Summary:        Header-only C++ SHA-256 implementation
License:        MIT
URL:            https://github.com/okdshin/PicoSHA2
Source0:        picosha2-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
Provides:       picosha2-devel = %{version}-%{release}

%description
PicoSHA2 is a header-only SHA-256 implementation using standard C++ libraries.

%package tests
Summary:        Original PicoSHA2 test source for installed-header verification
Requires:       %{name} = %{version}-%{release}
Requires:       gcc-c++

%description tests
Unmodified upstream test source, replayed against the installed public header.

%prep
%autosetup -n PicoSHA2-%{upstream_commit}

%build
cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=None \
    -DCMAKE_CXX_FLAGS='%{optflags} -UNDEBUG' \
    -DPICOSHA2_TEST=ON -DPICOSHA2_EXAMPLE=ON
cmake --build build --parallel %{_smp_build_ncpus}

%install
install -Dpm0644 picosha2.h %{buildroot}%{_includedir}/picosha2.h
install -Dpm0644 test/test.cpp %{buildroot}%{_datadir}/picosha2/qa/test.cpp
cmp test/test.cpp %{buildroot}%{_datadir}/picosha2/qa/test.cpp
cmp picosha2.h %{buildroot}%{_includedir}/picosha2.h

%check
# The original file-stream tests read test.cpp from the runtime working directory.
# Keep its exact bytes in the original registered CTest's build working directory.
cp -p test/test.cpp build/test/test.cpp
ctest --test-dir build/test --output-on-failure --no-tests=error -V > original-ctest.log 2>&1
cat original-ctest.log
test "$(grep -c ' is succeeded\.' original-ctest.log)" -eq 202
! grep -F ' is failed.' original-ctest.log
grep -F '100% tests passed, 0 tests failed out of 1' original-ctest.log
run_installed_defaults() {
    root="$1"
    work="$(mktemp -d)"
    mkdir "$work/test"
    cp "$root%{_datadir}/picosha2/qa/test.cpp" "$work/test/test.cpp"
    test -s "$work/test/test.cpp"
    ln -s "$root%{_includedir}/picosha2.h" "$work/picosha2.h"
    g++ %{optflags} -UNDEBUG "$work/test/test.cpp" -o "$work/unittest"
    (cd "$work/test" && "$work/unittest") > "$work/original.log" 2>&1
    cat "$work/original.log"
    test "$(grep -c ' is succeeded\.' "$work/original.log")" -eq 202
    ! grep -F ' is failed.' "$work/original.log"
}
run_installed_defaults '%{buildroot}'

%files
%license LICENSE
%doc README.md
%{_includedir}/picosha2.h

%files tests
%license LICENSE
%dir %{_datadir}/picosha2
%dir %{_datadir}/picosha2/qa
%{_datadir}/picosha2/qa/test.cpp

%changelog
* Sun Oct 18 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.1-1
- Preserve all original tests and example build targets from the fixed official release.
- Replay all 202 original checks with a failure-sensitive output oracle and installed header.
