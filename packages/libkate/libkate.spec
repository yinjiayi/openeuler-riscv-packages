# SPDX-License-Identifier: Apache-2.0
Name:           libkate
Version:        0.4.3
Release:        1%{?dist}
Summary:        Kate text and subtitle codec with Ogg integration
License:        BSD-3-Clause
URL:            https://wiki.xiph.org/Kate
Source0:        libkate-%{version}.tar.gz

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libogg-devel
BuildRequires:  libpng-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
libkate encodes and decodes timed text and subtitles in the Kate bitstream
format. It also provides an Ogg interface and command-line tools.

%package devel
Summary:        Development files for libkate
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libogg-devel%{?_isa}
Requires:       pkgconf-pkg-config

%description devel
Public Kate and Ogg-Kate headers, linker names, pkg-config metadata, and
upstream API documentation.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-doc
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Preserve registered tests plus upstream Kate/Ogg and SRT/LRC round trips.
# Assert a CLI round trip because an upstream loop can mask a case failure.
%make_build check
./tools/kateenc -s 0 -c test -l en -K 5 -R 15 -t kate \
  -o kate-roundtrip.ogg examples/kate/minimal.kate
./tools/katedec -o kate-roundtrip.kate kate-roundtrip.ogg
grep -F 'plain old text' kate-roundtrip.kate
./tools/kateenc --version | grep -F '%{version}'

%files
%license COPYING
%{_libdir}/libkate.so.1*
%{_libdir}/liboggkate.so.1*
%{_bindir}/kateenc
%{_bindir}/katedec
%{_bindir}/katalyzer
%{_mandir}/man1/kateenc.1*
%{_mandir}/man1/katedec.1*
%{_mandir}/man1/katalyzer.1*
%{_mandir}/man1/KateDJ.1*

%files devel
%license COPYING
%{_includedir}/kate/
%{_libdir}/libkate.so
%{_libdir}/liboggkate.so
%{_libdir}/pkgconfig/kate.pc
%{_libdir}/pkgconfig/oggkate.pc
%{_docdir}/libkate/

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.3-1
- Initial openEuler RISC-V package with Kate/Ogg round-trip tests.
