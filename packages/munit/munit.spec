# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# Source-distributed API and source-only QA: no installed ELF to split.
%global debug_package %{nil}
%global upstream_commit ad67a3a2ca6b0e106c9c8d515772359eadcefad6
Name:           munit
Version:        0.2.0
Release:        1%{?dist}
Summary:        Small source-distributed C unit testing framework
License:        MIT
URL:            https://nemequ.github.io/munit/
Source0:        https://codeload.github.com/nemequ/munit/tar.gz/%{upstream_commit}#/munit-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  findutils
BuildRequires:  rpm

%description
Munit is a C unit testing framework distributed as a header and a C source
file, as recommended by upstream. Consumers compile munit.c with their tests.
All original sources and default example tests are retained unchanged.

%package tests
Summary:        Complete original Munit example test sources
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       make
Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       rpm

%description tests
Original example and Makefile to rebuild against the installed public header
and C source. The unchanged default suite covers two ordinary cases and nine
parameter combinations. No executable is installed and no test is filtered.
Wall/CPU time printed by the framework is not native performance validation.

%prep
%setup -q -n %{name}-%{upstream_commit}

%build
# Retain upstream's c99/debug defaults, adding distribution optimization flags.
%make_build CC=gcc CFLAGS="%{optflags} -std=c99 -g"

%install
install -d %{buildroot}%{_includedir} %{buildroot}%{_datadir}/%{name}/qa
install -m 0644 munit.h %{buildroot}%{_includedir}/munit.h
install -m 0644 munit.c %{buildroot}%{_datadir}/%{name}/munit.c
install -m 0644 example.c Makefile COPYING %{buildroot}%{_datadir}/%{name}/qa/

%check
# The original test target has no filters, seed override or no-fork override.
make test > original-tests.log 2>&1
cat original-tests.log
grep -Fx '11 of 11 (100%%) tests successful, 0 (0%%) test skipped.' original-tests.log
# Replay the original Makefile with the staged installed public source/header.
qa=$(mktemp -d)
cp %{buildroot}%{_includedir}/munit.h %{buildroot}%{_datadir}/%{name}/munit.c "$qa/"
cp %{buildroot}%{_datadir}/%{name}/qa/Makefile %{buildroot}%{_datadir}/%{name}/qa/example.c "$qa/"
make -C "$qa" CC=gcc CFLAGS="%{optflags} -std=c99 -g"
make -C "$qa" test > staged-tests.log 2>&1
cat staged-tests.log
grep -Fx '11 of 11 (100%%) tests successful, 0 (0%%) test skipped.' staged-tests.log
test "$(find %{buildroot} -type f | wc -l)" -eq 5

%files
%license COPYING
%doc README.md
%{_includedir}/munit.h
%{_datadir}/%{name}/munit.c

%files tests
%license COPYING
%{_datadir}/%{name}/qa/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 0.2.0-1
- Pin the official source and retain the full original default test suite.
- Ship the original source-distributed API and source-only installed QA.
