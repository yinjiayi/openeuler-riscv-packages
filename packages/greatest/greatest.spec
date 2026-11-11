# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Only public header and source-only QA are installed.
%global debug_package %{nil}
%global upstream_commit 11a6af1919049df502405913da64fb385c219361
Name:           greatest
Version:        1.5.0
Release:        1%{?dist}
Summary:        Single-header C unit testing framework
License:        ISC
URL:            https://github.com/silentbicycle/greatest
Source0:        https://codeload.github.com/silentbicycle/greatest/tar.gz/%{upstream_commit}#/greatest-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  rpm

%description
Greatest supplies a portable C unit testing framework in one public header.
The original example sources and Makefile are retained unchanged.

%package tests
Summary:        Unmodified Greatest default example sources
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       make
Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       rpm

%description tests
Source-only QA for the installed public header. The original examples
intentionally exercise failure and skip reporting. Acceptance verifies exact
default counts and exit codes, including all random cases and slow Fibonacci
cases, rather than requiring intentionally negative examples to return zero.

%prep
%setup -q -n %{name}-%{upstream_commit}

%build
# Keep the complete original five-C default plus original C++ example.
env -u CFLAGS -u CXXFLAGS -u CPPFLAGS -u LDFLAGS -u COMMON_FLAGS -u MAKEFLAGS -u MFLAGS -u GNUMAKEFLAGS -u MAKEFILES make all all_cpp CC=gcc CXX=g++

%install
install -d %{buildroot}%{_includedir} %{buildroot}%{_datadir}/%{name}/qa
install -m 0644 greatest.h %{buildroot}%{_includedir}/greatest.h
install -m 0644 Makefile example*.c example_cpp.cpp %{buildroot}%{_datadir}/%{name}/qa/

%check
# The examples intentionally demonstrate failures and skips. Check exact
# default counts and exit codes; never turn an arbitrary failure into success.
run_expected() {
    name=$1 total=$2 passed=$3 failed=$4 skipped=$5 expected_rc=$6
    if "./$name" > "$name.log" 2>&1; then rc=0; else rc=$?; fi
    cat "$name.log"
    test "$rc" -eq "$expected_rc"
    test "$(grep -Ec "^Total: $total tests? " "$name.log")" -eq 1
    test "$(grep -Fxc "Pass: $passed, fail: $failed, skip: $skipped." "$name.log")" -eq 1
}
run_all_defaults() (
    cd "$1"
    unset CFLAGS CXXFLAGS CPPFLAGS LDFLAGS COMMON_FLAGS MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEFILES
    export LC_ALL=C
    make all all_cpp CC=gcc CXX=g++
    # An independent stdlib-only process observes this target libc's default
    # rand sequence. No greatest header, reseeding or symbol interposition.
    cat > rand-oracle.c <<'ORACLE'
#include <stdio.h>
#include <stdlib.h>
int main(void) {
    unsigned int i, pass = 9, fail = 20, skip = 2, total = 231;
#if !defined(__STDC_VERSION__) || __STDC_VERSION__ < 19901L
    pass--; fail--; total -= 2;
#endif
    for (i = 0; i < 200; i++) {
        int r = rand() %% 10;
        if (r == 0) fail++;
        else if (r == 1) skip++;
        else pass++;
    }
    if (pass + fail + skip != total) return 2;
    printf("%%u %%u %%u %%u\n", total, pass, fail, skip);
    return 0;
}
ORACLE
    gcc -Wall -Wextra -pedantic -Werror rand-oracle.c -o rand-oracle
    ./rand-oracle > rand-expected.txt
    read -r total passed failed skipped < rand-expected.txt
    run_expected example "$total" "$passed" "$failed" "$skipped" 1
    run_expected example_no_suite 3 1 1 1 1
    run_expected example_no_runner 1 1 0 0 0
    run_expected example_shuffle 1066 1064 2 0 1
    run_expected example_trunc 11 11 0 0 0
    run_expected example_cpp 1 0 1 0 1
    grep -Fx 'pass 1, fail 0, skip 0, assertions 0' example_no_runner.log
    grep -Fx 'fib 39 -> 102334155' example.log
    echo 'PASS greatest six original default examples; exact counts and exits'
)

run_all_defaults "$PWD"
qa=$(mktemp -d)
cp %{buildroot}%{_includedir}/greatest.h "$qa/"
cp %{buildroot}%{_datadir}/%{name}/qa/* "$qa/"
run_all_defaults "$qa"

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_includedir}/greatest.h

%files tests
%license LICENSE
%{_datadir}/%{name}/qa/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.5.0-1
- Pin official source and preserve all original default examples and warnings.
- Verify exact negative-example outcomes against staged and installed headers.
