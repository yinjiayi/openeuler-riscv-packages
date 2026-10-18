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
# Do not replace CXX with none, filter TESTS, or globally remove -Werror.
env -u CFLAGS -u CXXFLAGS -u MAKEFLAGS -u MFLAGS -u GNUMAKEFLAGS -u MAKEFILES make -C test all CC=gcc CXX=g++
test "$(find test -maxdepth 1 -type f -perm /111 | wc -l)" -eq 70
# Replay the entire original all target with the staged installed header.
qa=$(mktemp -d)
cp %{buildroot}%{_includedir}/hedley.h "$qa/"
cp -a %{buildroot}%{_datadir}/%{name}/qa/test "$qa/test"
env -u CFLAGS -u CXXFLAGS -u MAKEFLAGS -u MFLAGS -u GNUMAKEFLAGS -u MAKEFILES make -C "$qa/test" all CC=gcc CXX=g++
test "$(find "$qa/test" -maxdepth 1 -type f -perm /111 | wc -l)" -eq 70
echo 'PASS hedley original-default=70 staged-installed-header=70 compile-link-only'

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
