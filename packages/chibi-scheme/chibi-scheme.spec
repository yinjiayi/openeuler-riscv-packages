# SPDX-License-Identifier: Apache-2.0
Name:           chibi-scheme
Version:        0.12.0
Release:        1%{?dist}
Summary:        Small embeddable R7RS Scheme implementation
License:        BSD-3-Clause AND MIT AND LicenseRef-chibi-scheme-public-domain
URL:            https://github.com/ashinn/chibi-scheme
Source0:        chibi-scheme-0.12.0.tar.gz
Source1:        LICENSE-MIT-racket.txt
BuildRequires:  bash
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  sed
Requires:       bash
Requires:       coreutils
Requires:       grep

%description
Small embeddable R7RS Scheme implementation with the upstream default numeric
tower, Unicode support, shared module libraries, headers, FFI and documentation
tools. Includes the unchanged default R7RS suite for installed validation.

%prep
%autosetup -n chibi-scheme-08e23be118e7de8cf29d606bc4793371c0ace680 -p1
test "$(head -n 1 VERSION)" = '%{version}'
# Preserve every original notice and its surrounding attribution before building.
mkdir original-notices
find . -type f ! -path './original-notices/*' \
    -exec cp --parents '{}' original-notices/ ';'
find original-notices -type f -exec chmod 0644 '{}' ';'
cp %{SOURCE1} LICENSE-MIT-racket.txt

%build
# No feature overrides: use the original all target and detected Linux platform.
%make_build PREFIX=%{_prefix} LIBDIR=%{_libdir} SOLIBDIR=%{_libdir} \
    CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}"

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir} SOLIBDIR=%{_libdir} \
    CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}"
install -Dm644 tests/r7rs-tests.scm \
    %{buildroot}%{_datadir}/chibi-scheme-tests/r7rs-tests.scm
(
    cd %{buildroot}%{_datadir}/chibi-scheme-tests
    sha256sum r7rs-tests.scm > SHA256SUMS
)

%check
set -eu
export LC_ALL=C
unset TEST_FILTER TEST_REMOVE TEST_GROUP_FILTER TEST_GROUP_REMOVE
# Upstream's unchanged default target is test -> test-r7rs.
%make_build test PREFIX=%{_prefix} LIBDIR=%{_libdir} SOLIBDIR=%{_libdir} \
    CC=gcc CFLAGS="%{optflags}" LDFLAGS="%{?build_ldflags}"
# The original suite prints failures without calling test-exit. Replay the same
# unmodified suite with its own exported test-exit to enforce a failing status.
CHIBI_IGNORE_SYSTEM_PATH=1 CHIBI_MODULE_PATH=lib LD_LIBRARY_PATH=. \
    ./chibi-scheme -mchibi.test -I tests -l r7rs-tests.scm -e '(test-exit)'

%files
%license COPYING AUTHORS LICENSE-MIT-racket.txt original-notices
%doc README.md RELEASE
%{_bindir}/chibi-scheme
%{_bindir}/chibi-ffi
%{_bindir}/chibi-doc
%{_bindir}/snow-chibi
%{_bindir}/snow-chibi.scm
%{_libdir}/libchibi-scheme.so
%{_libdir}/libchibi-scheme.so.0
%{_libdir}/libchibi-scheme.so.%{version}
%{_libdir}/chibi
%{_libdir}/pkgconfig/chibi-scheme.pc
%{_includedir}/chibi
%{_datadir}/chibi
%{_datadir}/chibi-scheme-tests
%{_mandir}/man1/chibi-scheme.1*
%{_mandir}/man1/chibi-ffi.1*
%{_mandir}/man1/chibi-doc.1*

%changelog
* Sat Oct 24 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.12.0-1
- Preserve default build, modules and R7RS tests with strict installed replay.
