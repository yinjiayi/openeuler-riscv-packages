# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Upstream installs a static development library, no standalone ELF payload.
%global debug_package %{nil}
%global upstream_commit 0fbac1a0c6ebb7ecd72f0d7ae89c2b79eb3a12eb
Name:           cargs
Version:        1.2.0
Release:        1%{?dist}
Summary:        Small portable C argument parsing library
License:        MIT
URL:            https://likle.github.io/cargs/
Source0:        https://codeload.github.com/likle/cargs/tar.gz/%{upstream_commit}#/cargs-%{version}.tar.gz
Patch0:         0001-use-configured-pkgconfig-libdir.patch
BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  binutils
BuildRequires:  rpm
Provides:       cargs-devel = %{version}-%{release}
Provides:       cargs-static = %{version}-%{release}

%description
Cargs is a small C command-line argument parsing library. This package keeps
the original static-library installation, public header and CMake/pkg-config
development metadata. Official tag v1.2.0 retains upstream project version
1.1.0 in its build metadata; this recipe does not rewrite that version.

%package tests
Summary:        Original Cargs default test sources
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       cmake
Requires:       make
Requires:       pkgconf-pkg-config
Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       binutils
Requires:       rpm

%description tests
Original test source files and the complete generated upstream 23-case test
registry. Rebuild and replay the bare original runner against the installed
library, then replay all individual cases without filters or feature macros.

%prep
%autosetup -p1 -n %{name}-%{upstream_commit}

%build
# Preserve upstream static default, C11, assertions and strict warning policy.
cmake -S . -B build -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_lib} -DCMAKE_C_FLAGS="%{optflags}" -DENABLE_TESTS=1 -DENABLE_DEMO=1
cmake --build build --verbose %{?_smp_mflags}

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/%{name}/qa
install -m 0644 test/main.c test/option_test.c test/definitions.h test/tests.h %{buildroot}%{_datadir}/%{name}/qa/

%check
export LC_ALL=C
# Unfiltered original CTest registry and bare runner; all assertions retained.
(cd build && ctest --output-on-failure) > ctest.log 2>&1
cat ctest.log
grep -Fx '100%% tests passed, 0 tests failed out of 23' ctest.log
test "$(grep -Ec '^[[:space:]]*[0-9]+/23 Test' ctest.log)" -eq 23
./build/cargstest > original-runner.log 2>&1
cat original-runner.log
grep -Fx '23/23 (100.00%%) of those tests succeeded.' original-runner.log
test "$(grep -Ec "^ Running 'option/.* SUCCESS$" original-runner.log)" -eq 23
./build/cargsdemo -s -M --long --key=value extra > original-demo.log
cat original-demo.log
grep -Fx 'simple_flag: 1, multiple_flag: 1, long_flag: 1, key: value' original-demo.log
grep -Fx 'additional parameter: extra' original-demo.log

run_installed_defaults() (
    root=$1
    qa=$root/usr/share/cargs/qa
    test -f "$root/usr/lib64/libcargs.a"
    export LC_ALL=C
    export PKG_CONFIG_LIBDIR="$root/usr/lib64/pkgconfig"
    export PKG_CONFIG_SYSROOT_DIR="$root"
    test "$(pkg-config --modversion cargs)" = 1.1.0
    test "$(pkg-config --variable=libdir cargs)" = "$root/usr/lib64"
    work=$(mktemp -d)
    cd "$work"
    # No source implementation is distributed with QA; link the installed .a.
    gcc -std=c11 -Wall -Wextra -Werror -Wpedantic $(pkg-config --cflags cargs) "$qa/main.c" "$qa/option_test.c" $(pkg-config --static --libs cargs) -o cargstest
    ./cargstest > all.log 2>&1
    cat all.log
    grep -Fx '23/23 (100.00%%) of those tests succeeded.' all.log
    test "$(grep -Ec "^ Running 'option/.* SUCCESS$" all.log)" -eq 23
    # Replay every original registry entry as well, without modifying tests.h.
    grep -E '^  XX\(option,[a-z_]+\) ' "$qa/tests.h" > registry.txt
    test "$(wc -l < registry.txt)" -eq 23
    while IFS= read -r entry; do
        name=${entry#*XX(option,}
        name=${name%%)*}
        ./cargstest option "$name" > "case-$name.log" 2>&1
        cat "case-$name.log"
        grep -Fx 'The test has been executed.' "case-$name.log"
        test "$(grep -Ec "^ Running 'option/.* SUCCESS$" "case-$name.log")" -eq 1
    done < registry.txt
    echo 'PASS cargs installed static library: all 23 original default cases'
)
run_installed_defaults '%{buildroot}'

%files
%license LICENSE.md
%doc README.md
%{_includedir}/cargs.h
%{_libdir}/libcargs.a
%{_libdir}/pkgconfig/cargs.pc
%{_libdir}/cmake/cargs/

%files tests
%license LICENSE.md
%{_datadir}/%{name}/qa/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.2.0-1
- Pin official source; preserve original static defaults and all 23 tests.
- Correct pkg-config libdir and replay original tests against installed bytes.
