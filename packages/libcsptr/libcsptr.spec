# SPDX-License-Identifier: MIT
# Copyright (c) 2026 yinjiayi
# The upstream default is only a static archive, no separate ELF debuginfo.
# Keep original -g and all original compiler flags in the archive.
%global debug_package %{nil}
%global upstream_commit 82d3b1beafe7ed9f13f75e0d3367c60205e10f27

Name:           libcsptr
Version:        2.0.4
Release:        1%{?dist}
Summary:        Smart pointers and reference-counted arrays for GNU C
License:        MIT AND BSD-3-Clause AND (GPL-3.0-or-later WITH Autoconf-exception-macro)
URL:            https://github.com/Snaipe/libcsptr
Source0:        https://codeload.github.com/snaipe/libcsptr/tar.gz/%{upstream_commit}#/libcsptr-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/libssh/libssh-mirror/07430deb9b97b751ec5ea5a7fc307f40bf042e0a/cmake/Modules/COPYING-CMAKE-SCRIPTS
Source2:        https://ftp.gnu.org/gnu/Licenses/gpl-3.0.txt#/GPL-3.0.txt
Patch0:         0001-honor-GNUInstallDirs.patch
Patch1:         0002-handle-shared-array-kind-and-destructor-metadata.patch
Patch2:         0003-add-installed-QA.patch

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  check-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  glibc-devel
BuildRequires:  python3
BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  grep
BuildRequires:  binutils

%description
GNU C smart pointers with automatic cleanup, custom destructors, caller
metadata, unique/shared ownership and length-aware arrays. Retains the
original default static archive, five public headers and manual page.
The library and public API are MIT. BSD terms cover the CMake Check finder;
GPL3 with the original Autoconf macro exception covers only unused source
build auxiliary m4/ax_prefix_config_h.m4, not the static library's API.

%package tests
Summary:        Complete original libcsptr Check suite and installed checks
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gcc
Requires:       glibc-devel
Requires:       check-devel
Requires:       pkgconf-pkg-config
Requires:       bash
Requires:       coreutils
Requires:       grep
Requires:       rpm
Requires:       binutils

%description tests
All five unchanged upstream C test files and their two original headers,
with all twelve original Check cases. Additional downstream shared-array
and installed-header/static-archive checks do not replace the original suite.

%prep
%setup -q -n %{name}-%{upstream_commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1
install -d distribution-licenses
install -m 0644 %{SOURCE1} distribution-licenses/COPYING-CMAKE-SCRIPTS
install -m 0644 %{SOURCE2} distribution-licenses/GPL-3.0.txt
# Record precisely all unchanged original test inputs, no generated fixture.
(cd check/test && sha256sum array.c misc.c scalar.c shared.c test.c test.h utils.h) > downstream/SHA256SUMS

%build
# Fail closed if Check is missing; upstream otherwise silently omits its suite.
pkg-config --exists check
cmake -S . -B build \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=lib64 \
    -DCMAKE_C_FLAGS="%{optflags}" \
    -DCMAKE_C_FLAGS_RELWITHDEBINFO="%{optflags} -UNDEBUG" \
    -DCMAKE_REQUIRE_FIND_PACKAGE_Check=TRUE \
    -DTESTS=ON -DSENTINEL=ON -DFIXED_ALLOCATOR=OFF
cmake --build build --parallel %{?_smp_build_ncpus}
test -x build/check/check_unit
test -f build/libcsptr.a
grep -Fx 'TESTS:BOOL=ON' build/CMakeCache.txt
grep -Fx 'SENTINEL:BOOL=ON' build/CMakeCache.txt
grep -Fx 'FIXED_ALLOCATOR:BOOL=OFF' build/CMakeCache.txt

%install
DESTDIR=%{buildroot} cmake --install build
install -d %{buildroot}%{_datadir}/%{name}/tests/original
install -m 0644 check/test/array.c check/test/misc.c check/test/scalar.c \
    check/test/shared.c check/test/test.c check/test/test.h check/test/utils.h \
    %{buildroot}%{_datadir}/%{name}/tests/original/
install -m 0644 downstream/SHA256SUMS downstream/consumer.c %{buildroot}%{_datadir}/%{name}/tests/
install -m 0755 downstream/run-tests.sh %{buildroot}%{_datadir}/%{name}/run-tests.sh

%check
ctest --test-dir build --show-only=json-v1 > build/ctest-registered.json
python3 - <<'PY'
import json
from pathlib import Path
tests = json.loads(Path('build/ctest-registered.json').read_text())['tests']
assert len(tests) == 1 and tests[0]['name'] == 'check_unit'
assert Path(tests[0]['command'][0]).name == 'check_unit'
PY
ctest --test-dir build --output-on-failure
bash %{buildroot}%{_datadir}/%{name}/run-tests.sh --staged %{buildroot}

%files
%license LICENSE distribution-licenses/ .cmake/Modules/FindCheck.cmake
%license .cmake/Modules/Coveralls.cmake .cmake/Modules/CoverallsClear.cmake .cmake/Modules/CoverallsGenerateGcov.cmake
%license m4/ax_prefix_config_h.m4
%doc README.md
%{_libdir}/libcsptr.a
%{_includedir}/csptr/
%{_mandir}/man3/csptr.3*

%files tests
%{_datadir}/%{name}/

%changelog
* Sun Oct 18 2026 yinjiayi <yinjiayi@users.noreply.github.com> - 2.0.4-1
- Preserve all upstream defaults and original tests; package installed QA.
- Fix shared-array flag/header handling and honor standard multilib directory.
