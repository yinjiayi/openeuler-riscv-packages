# SPDX-License-Identifier: Apache-2.0
Name:           jbig2dec
Version:        0.20
Release:        1%{?dist}
Summary:        JBIG2 bi-level image decoder library and utility
License:        AGPL-3.0-or-later
URL:            https://github.com/ArtifexSoftware/jbig2dec
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  libpng-devel
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  python3
BuildRequires:  zlib-devel

%description
Jbig2dec is a decoder library and utility for the JBIG2 bi-level image
compression standard, also known as ITU T.88 and ISO/IEC 14492.

%package devel
Summary:        Development files for jbig2dec
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
The public header, pkg-config metadata, and unversioned shared-library link
for developing applications with jbig2dec.

%prep
%autosetup -p1
%{__sed} -i '1s|^#! */usr/bin/env python$|#!/usr/bin/python3|' test_jbig2dec.py

%build
%configure --disable-static --with-libpng
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
# Run every maintained upstream test target, including the Python decoder
# corpus and the SHA-1, Huffman, and arithmetic unit tests.
%make_build check

%files
%license LICENSE COPYING
%doc README CHANGES
%{_bindir}/jbig2dec
%{_libdir}/libjbig2dec.so.0*
%{_mandir}/man1/jbig2dec.1*

%files devel
%license LICENSE COPYING
%{_includedir}/jbig2.h
%{_libdir}/libjbig2dec.so
%{_libdir}/pkgconfig/jbig2dec.pc

%changelog
* Fri Aug 14 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.20-1
- Initial openEuler RISC-V package from reviewed upstream evidence.
