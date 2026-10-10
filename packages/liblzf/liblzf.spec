# SPDX-License-Identifier: Apache-2.0
Name:           liblzf
Version:        3.6
Release:        1%{?dist}
Summary:        Small LZF compression library
License:        BSD-2-Clause
URL:            https://software.schmorp.de/pkg/liblzf.html
Source0:        liblzf-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
LibLZF provides fast, small-footprint, lossless compression and decompression.
This package contains the shared library.

%package devel
Summary:        Development files for LibLZF
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The C header and linker name for developing applications using LibLZF.

%package tools
Summary:        LZF compression and decompression command-line utility
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
The upstream lzf command-line compressor and decompressor.

%prep
%autosetup -p1

%build
%configure
%make_build CFLAGS="%{optflags} -fPIC" LDFLAGS="%{build_ldflags}"
gcc -shared %{build_ldflags} -Wl,-soname,liblzf.so.1 \
  -o liblzf.so.1.0.0 lzf_c.o lzf_d.o
ln -s liblzf.so.1.0.0 liblzf.so.1
ln -s liblzf.so.1 liblzf.so
gcc %{build_ldflags} -o lzf lzf.o -L. -llzf

%install
install -Dpm0755 liblzf.so.1.0.0 %{buildroot}%{_libdir}/liblzf.so.1.0.0
ln -s liblzf.so.1.0.0 %{buildroot}%{_libdir}/liblzf.so.1
ln -s liblzf.so.1 %{buildroot}%{_libdir}/liblzf.so
install -Dpm0644 lzf.h %{buildroot}%{_includedir}/lzf.h
install -Dpm0755 lzf %{buildroot}%{_bindir}/lzf

%check
printf 'liblzf-test-00000000000000000000000000000000\n' > expected.txt
LD_LIBRARY_PATH="$PWD" ./lzf < expected.txt > expected.lzf
LD_LIBRARY_PATH="$PWD" ./lzf -d < expected.lzf > actual.txt
cmp expected.txt actual.txt

%files
%license LICENSE
%doc README Changes
%{_libdir}/liblzf.so.1*

%files devel
%license LICENSE
%{_includedir}/lzf.h
%{_libdir}/liblzf.so

%files tools
%license LICENSE
%{_bindir}/lzf

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.6-1
- Package the official LibLZF 3.6 release for openEuler RISC-V.
