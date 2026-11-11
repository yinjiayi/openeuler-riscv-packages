# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Static development payload only; no installed ELF or generated debug namespace.
%global debug_package %{nil}
%global upstream_commit 6d2233ce14dca063994708a91b3b98e24e8aa0c3
Name:           tinyexpr
Version:        1.1.1
Release:        1%{?dist}
Summary:        Tiny C mathematical expression parser and evaluator
License:        Zlib
URL:            https://codeplea.com/tinyexpr
Source0:        https://codeload.github.com/codeplea/tinyexpr/tar.gz/%{upstream_commit}#/tinyexpr-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  binutils
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  glibc-langpack-de
Provides:       tinyexpr-devel = %{version}-%{release}
Provides:       tinyexpr-static = %{version}-%{release}

%description
Tinyexpr parses, compiles and evaluates mathematical expressions in C.
This package supplies the public header and a static development archive.
Link consumers with -ltinyexpr -lm. The upstream project has no install target.

%package tests
Summary:        Unmodified Tinyexpr default smoke test sources
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       glibc-langpack-de

%description tests
Original smoke.c and minctest.h. Rebuild all 15 original default test groups
against the installed static archive and header; require the locale group
to run, not skip. The alternate pow/log mode is additionally tested by the
unmodified upstream make all during the package build.

%prep
%autosetup -n %{name}-%{upstream_commit}

%build
# Upstream all builds seven programs and executes both original smoke variants.
# Keep original warnings/optimization and add distribution hardening flags.
export LC_ALL=C
make all CC=gcc CCFLAGS="-Wall -Wshadow -O2 %{optflags}" > original-build.log 2>&1
cat original-build.log
test "$(grep -Ec '^ALL TESTS PASSED \([0-9]+/[0-9]+\)$' original-build.log)" -eq 2
test "$(grep -Ec '^[[:space:]]*(Results|Syntax|NaNs|INFs|Variables|Functions|Dynamic|Closure|Optimize|Pow|Combinatorics|Logic|Depth|Number|Locale)[[:space:]]+pass:' original-build.log)" -eq 30
if grep -Ei 'skipping|SOME TESTS FAILED|FAILED:' original-build.log; then exit 1; fi
# Archive the original default object already built by upstream all.
ar rcs libtinyexpr.a tinyexpr.o

%install
install -Dpm 0644 tinyexpr.h %{buildroot}%{_includedir}/tinyexpr.h
install -Dpm 0644 libtinyexpr.a %{buildroot}%{_libdir}/libtinyexpr.a
install -d %{buildroot}%{_datadir}/%{name}/qa
install -pm 0644 smoke.c minctest.h %{buildroot}%{_datadir}/%{name}/qa/

%check
export LC_ALL=C
# Re-run both bare original smoke binaries, without editing/filtering the suite.
for runner in smoke smoke_pr; do
    ./$runner > "$runner.log" 2>&1
    cat "$runner.log"
    test "$(grep -Ec '^ALL TESTS PASSED \([0-9]+/[0-9]+\)$' "$runner.log")" -eq 1
    test "$(grep -Ec '^[[:space:]]*(Results|Syntax|NaNs|INFs|Variables|Functions|Dynamic|Closure|Optimize|Pow|Combinatorics|Logic|Depth|Number|Locale)[[:space:]]+pass:' "$runner.log")" -eq 15
    if grep -Ei 'skipping|SOME TESTS FAILED|FAILED:' "$runner.log"; then exit 1; fi
done
run_installed_defaults() (
    root=$1
    test -f "$root/usr/include/tinyexpr.h"
    test -f "$root/usr/lib64/libtinyexpr.a"
    qa=$root/usr/share/tinyexpr/qa
    work=$(mktemp -d)
    cd "$work"
    # No implementation source is in QA: the original test links installed .a.
    gcc -Wall -Wshadow -O2 -I"$root/usr/include" "$qa/smoke.c" "$root/usr/lib64/libtinyexpr.a" -lm -o smoke
    ./smoke > original-default.log 2>&1
    cat original-default.log
    test "$(grep -Ec '^ALL TESTS PASSED \([0-9]+/[0-9]+\)$' original-default.log)" -eq 1
    test "$(grep -Ec '^[[:space:]]*(Results|Syntax|NaNs|INFs|Variables|Functions|Dynamic|Closure|Optimize|Pow|Combinatorics|Logic|Depth|Number|Locale)[[:space:]]+pass:' original-default.log)" -eq 15
    if grep -Ei 'skipping|SOME TESTS FAILED|FAILED:' original-default.log; then exit 1; fi
    echo 'PASS tinyexpr installed static archive: all 15 original default groups'
)
run_installed_defaults '%{buildroot}'

%files
%license LICENSE
%doc README.md
%{_includedir}/tinyexpr.h
%{_libdir}/libtinyexpr.a

%files tests
%license LICENSE
%{_datadir}/%{name}/qa/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 1.1.1-1
- Pin official source and preserve both original smoke modes and default targets.
- Install static development bytes; replay unmodified tests against them.
