# SPDX-License-Identifier: Apache-2.0
Name:           libgrapheme
Version:        3.0.0
Release:        1%{?dist}
Summary:        Unicode string segmentation and case conversion library
License:        ISC AND Unicode-3.0
URL:            https://libs.suckless.org/libgrapheme/
Source0:        libgrapheme-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
libgrapheme provides Unicode string segmentation, UTF-8 encoding, and case
conversion through a small C99 library.

%package devel
Summary:        Development files for libgrapheme
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The public C header, pkg-config metadata, manual pages, and linkable library.

%prep
%autosetup

%build
./configure
%make_build CC=%{__cc} BUILD_CC=%{__cc} \
  CFLAGS='%{optflags} -std=c99 -Wno-overlength-strings' \
  BUILD_CFLAGS='%{optflags} -std=c99 -Wno-overlength-strings' \
  LDFLAGS='%{?build_ldflags}' BUILD_LDFLAGS='%{?build_ldflags}'

%install
%make_install PREFIX=%{_prefix} INCPREFIX=%{_includedir} \
  LIBPREFIX=%{_libdir} MANPREFIX=%{_mandir} \
  PCPREFIX=%{_libdir}/pkgconfig LDCONFIG=

%check
# Build the exact eight programs in upstream's test target, then execute each
# with fail-fast behavior. Upstream's plain shell loop can mask an earlier
# failure if a later program succeeds. No conformance case is excluded.
%make_build test/bidirectional test/case test/character test/line \
  test/sentence test/utf8-encode test/utf8-decode test/word
set -e
for program in test/bidirectional test/case test/character test/line \
  test/sentence test/utf8-encode test/utf8-decode test/word; do
  ./$program
done

%files
%license LICENSE data/LICENSE
%doc README
%{_libdir}/libgrapheme.so.3*

%files devel
%license LICENSE data/LICENSE
%{_includedir}/grapheme.h
%{_libdir}/libgrapheme.so
%{_libdir}/libgrapheme.a
%{_libdir}/pkgconfig/libgrapheme.pc
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.0-1
- Package official libgrapheme 3.0.0 with complete upstream tests.
