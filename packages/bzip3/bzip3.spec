# SPDX-License-Identifier: Apache-2.0
Name:           bzip3
Version:        1.5.3
Release:        1%{?dist}
Summary:        Modern block-sorting compression utility and library
License:        LGPL-3.0-or-later AND Apache-2.0 AND BSD-2-Clause
URL:            https://github.com/kspalaiologos/bzip3
Source0:        bzip3-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
bzip3 is a block-sorting compressor that combines a Burrows-Wheeler transform,
context mixing, and Lempel-Ziv-style prediction. This package provides the
command-line tools and shared library.

%package devel
Summary:        Development files for bzip3
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, CMake metadata, pkg-config metadata, and the unversioned shared-library
link for developing software with libbzip3.

%prep
%autosetup -p1

%build
%cmake \
  -DBUILD_SHARED_LIBS=ON \
  -DBZIP3_BUILD_APPS=ON \
  -DBZIP3_ENABLE_PTHREAD=ON \
  -DBZIP3_ENABLE_ARCH_NATIVE=OFF
%make_build

%install
DESTDIR=%{buildroot} %{__cmake} --install .

%check
./bzip3 -V | grep -F '%{version}'
./bzip3 -d < %{_builddir}/%{name}-%{version}/examples/shakespeare.txt.bz3 | \
  cmp - %{_builddir}/%{name}-%{version}/examples/shakespeare.txt
rm -f roundtrip.txt roundtrip.txt.bz3 roundtrip.out
printf 'openEuler RVA23 bzip3 round trip\n' > roundtrip.txt
./bzip3 -e roundtrip.txt roundtrip.txt.bz3
./bzip3 -d roundtrip.txt.bz3 roundtrip.out
cmp roundtrip.txt roundtrip.out

%files
%license LICENSE 3rdparty/libsais-LICENSE
%doc NEWS PORTING.md README.md doc/
%{_bindir}/bunzip3
%{_bindir}/bz3cat
%{_bindir}/bz3grep
%{_bindir}/bz3less
%{_bindir}/bz3more
%{_bindir}/bz3most
%{_bindir}/bzip3
%{_libdir}/libbzip3.so.0*
%{_mandir}/man1/bunzip3.1*
%{_mandir}/man1/bz3*.1*
%{_mandir}/man1/bzip3.1*

%files devel
%license LICENSE 3rdparty/libsais-LICENSE
%{_includedir}/libbz3.h
%{_libdir}/libbzip3.so
%{_libdir}/pkgconfig/bzip3.pc
%{_libdir}/cmake/bzip3/

%changelog
* Thu Aug 13 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.3-1
- Initial openEuler RISC-V package.
