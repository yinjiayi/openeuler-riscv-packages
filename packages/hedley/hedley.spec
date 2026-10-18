# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Header and source-only QA: no installed ELF to split.
%global debug_package %{nil}
%global upstream_commit 8fb0604a8095f6c907378cc3f0391520ae843f6f
Name:           hedley
Version:        15
Release:        1%{?dist}
Summary:        Portable C and C++ compiler feature macros
License:        CC0-1.0
URL:            https://nemequ.github.io/hedley/
Source0:        https://codeload.github.com/nemequ/hedley/tar.gz/%{upstream_commit}#/hedley-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  rpm

%description
Hedley provides portable feature detection, annotations and compiler hints
in a single public C/C++ header. The original source is retained unchanged.

%package tests
Summary:        Original Hedley compiler conformance test sources
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       gcc-c++
Requires:       make
Requires:       bash
Requires:       coreutils
Requires:       findutils
Requires:       rpm

%description tests
Unmodified upstream Makefile and all C test inputs for installed-header QA.
The original all target compiles and links 35 C and 35 C++ programs, including
intentional diagnostic examples. They are compiler conformance tests, not
runtime tests: some programs intentionally contain runtime-unsafe examples.
The upstream per-target diagnostic exceptions are retained unchanged.

%prep
%setup -q -n %{name}-%{upstream_commit}

%build
# Header-only; run the original compiler conformance suite in %%check.

%install
install -d %{buildroot}%{_includedir} %{buildroot}%{_datadir}/%{name}/qa/test
install -m 0644 hedley.h %{buildroot}%{_includedir}/hedley.h
install -m 0644 test/Makefile test/*.c %{buildroot}%{_datadir}/%{name}/qa/test/

%check
# The three diagnostic C++ rules intentionally overwrite their C output names.
# Keep all 70 compiler invocations; require the exact 67 resulting executables.
verify_default_outputs() {
    for name in array-param assume cast concat const constant deprecated empty-bases fallthrough flags inline likely malloc message noinline no-escape no-return non-null predict printf-format pure require restrict returns-non-null sentinel static-assert stringify unknown-cpp-attributes unknown-pragmas unavailable unreachable unused-function visibility warn warn-unused-result; do
        test -x "$1/$name" || return 1
        case "$name" in
            unknown-pragmas|unavailable|warn) test ! -e "$1/$name-cpp" || return 1 ;;
            *) test -x "$1/$name-cpp" || return 1 ;;
        esac
    done
    test "$(find "$1" -maxdepth 1 -type f -perm /111 | wc -l)" -eq 67
}
# Do not replace CXX with none, filter TESTS, or globally remove -Werror.
env -u CFLAGS -u CXXFLAGS -u MAKEFLAGS -u MFLAGS -u GNUMAKEFLAGS -u MAKEFILES make -C test all CC=gcc CXX=g++
verify_default_outputs test
# Replay the entire original all target with the staged installed header.
qa=$(mktemp -d)
cp %{buildroot}%{_includedir}/hedley.h "$qa/"
cp -a %{buildroot}%{_datadir}/%{name}/qa/test "$qa/test"
env -u CFLAGS -u CXXFLAGS -u MAKEFLAGS -u MFLAGS -u GNUMAKEFLAGS -u MAKEFILES make -C "$qa/test" all CC=gcc CXX=g++
verify_default_outputs "$qa/test"
echo 'PASS hedley original-default=70 staged-installed-header=70 final-files=67 compile-link-only'

%files
%license COPYING
%doc README.md
%{_includedir}/hedley.h

%files tests
%license COPYING
%{_datadir}/%{name}/qa/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 15-1
- Pin the official stable source and preserve every original default target.
- Replay compiler conformance against staged and installed public headers.
