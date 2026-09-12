# SPDX-License-Identifier: Apache-2.0
Name:           lzlib
Version:        1.16
Release:        1%{?dist}
Summary:        Compression library for the lzip format
License:        BSD-2-Clause AND GPL-2.0-or-later
URL:            https://www.nongnu.org/lzip/lzlib.html
Source0:        lzlib-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
Lzlib is a C library providing in-memory LZMA compression and decompression
functions with integrity checking for the lzip format. This package also
contains the minilzip command-line utility.

%package devel
Summary:        Development files for lzlib
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, documentation, and the unversioned shared-library link for developing
applications with lzlib.

%prep
%autosetup -p1

%build
./configure \
  --prefix=%{_prefix} \
  --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} \
  --datarootdir=%{_datadir} \
  --includedir=%{_includedir} \
  --infodir=%{_infodir} \
  --libdir=%{_libdir} \
  --mandir=%{_mandir} \
  --enable-shared \
  CC="%{__cc}" \
  CFLAGS="%{optflags}" \
  LDFLAGS="%{build_ldflags}"
%make_build bin

%install
%make_install
%make_install install-bin
rm -f %{buildroot}%{_libdir}/liblz.a
rm -f %{buildroot}%{_infodir}/dir

%check
# Run the complete maintained upstream test script, including its library
# header/ABI consistency check and malformed-stream coverage.
%make_build check

%files
%license COPYING COPYING.GPL
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/minilzip
%{_libdir}/liblz.so.1*
%{_infodir}/lzlib.info*
%{_mandir}/man1/minilzip.1*

%files devel
%license COPYING
%doc doc/lzlib.texi
%{_includedir}/lzlib.h
%{_libdir}/liblz.so

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.16-1
- Initial openEuler RISC-V package from reviewed upstream evidence.
