# SPDX-License-Identifier: MIT AND LicenseRef-Public-Domain
%global debug_package %{nil}
%global upstream_commit 64d851a6f93267defcdc11cfaee4102786c660bb

Name:           libfixmath
Version:        0.20220222
Release:        1
Summary:        Q16.16 fixed point arithmetic static library
License:        MIT AND LicenseRef-Public-Domain
URL:            https://github.com/PetteriAimonen/libfixmath
Source0:        https://codeload.github.com/PetteriAimonen/libfixmath/tar.gz/%{upstream_commit}#/libfixmath-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.13
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  libubsan
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep

%description
Fixed point arithmetic with Q16.16 operations, public C and C++ headers and
the original default-configuration static development archive. The archive
name follows the unmodified upstream CMake output, liblibfixmath.a.

%package tests
Summary:        Original default-configuration tests for the installed archive
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       libubsan
Requires:       bash
Requires:       coreutils
Requires:       grep

%description tests
Unmodified original tests replayed against the installed default archive.
All twelve original instrumented CMake variants run separately during build.

%prep
%setup -q -n libfixmath-%{upstream_commit}

%build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_FLAGS_RELEASE='%{optflags} -UNDEBUG' -DCMAKE_CXX_FLAGS_RELEASE='%{optflags} -UNDEBUG'
cmake --build build --parallel %{?_smp_build_ncpus}
cmake --build build --target make_tests --parallel %{?_smp_build_ncpus}

%install
mkdir -p %{buildroot}%{_includedir}/libfixmath %{buildroot}%{_libdir}
install -pm0644 libfixmath/*.h libfixmath/*.hpp %{buildroot}%{_includedir}/libfixmath/
install -pm0644 build/liblibfixmath.a %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_datadir}/libfixmath/qa
install -pm0644 tests/*.c tests/*.h %{buildroot}%{_datadir}/libfixmath/qa/

%check
ctest --test-dir build -C Release --output-on-failure --no-tests=error -V > complete-ctest.log 2>&1
cat complete-ctest.log
grep -F '100% tests passed, 0 tests failed out of 12' complete-ctest.log
if grep -E 'runtime error:|AddressSanitizer:|UndefinedBehaviorSanitizer:' complete-ctest.log; then exit 1; fi
run_installed_defaults() {
    root=$1
    qa="$root/usr/share/libfixmath/qa"
    temp=$(mktemp -d)
    gcc -O2 -g -UNDEBUG -std=c11 -DPREFIX=ro64 -fsanitize=undefined -I"$root/usr/include" "$qa"/*.c "$root/usr/lib64/liblibfixmath.a" -lm -o "$temp/default-tests"
    "$temp/default-tests" > "$temp/default.log" 2>&1
    cat "$temp/default.log"
    if grep -E 'FAILED:|runtime error:|AddressSanitizer:|UndefinedBehaviorSanitizer:' "$temp/default.log"; then exit 1; fi
    for group in abs add mul div sub sqrt lerp macros; do
        grep -F "test_$group()" "$temp/default.log"
    done
    rm -f "$temp/default-tests" "$temp/default.log"
    rmdir "$temp"
    echo 'PASS libfixmath original-default=8 groups installed-static-archive skips=0'
}
run_installed_defaults '%{buildroot}'

%files
%license LICENSE AUTHORS libfixmath/fix16_fft.c
%doc README.md
%{_includedir}/libfixmath
%{_libdir}/liblibfixmath.a

%files tests
%license LICENSE AUTHORS libfixmath/fix16_fft.c
%{_datadir}/libfixmath

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.20220222-1
- Preserve all twelve original UBSan CTest variants and installed default tests.
