# SPDX-License-Identifier: Apache-2.0
Name:           libzip
Version:        1.11.4
Release:        1%{?dist}
Summary:        Library for reading, creating, and modifying ZIP archives
License:        BSD-3-Clause
URL:            https://libzip.org/
Source0:        libzip-%{version}.tar.xz
# Official nihtest release used only to retain libzip's complete regression suite.
Source1:        nihtest-1.9.1.tar.gz

BuildRequires:  bzip2-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  mandoc
BuildRequires:  openssl-devel
BuildRequires:  python3
BuildRequires:  python3-dateutil
BuildRequires:  tar
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  zstd-devel

%description
libzip is a C library for reading, creating, and modifying ZIP archives. It
supports multiple compression methods and authenticated encryption backends.

%package devel
Summary:        Development files for libzip
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config and CMake metadata, manual pages, and the unversioned
library link for developing applications with libzip.

%prep
%autosetup -p1
tar -xzf %{SOURCE1} -C %{_builddir}

%build
%{__mkdir_p} test-bin
printf '#!/usr/bin/env bash\nPYTHONPATH=%{_builddir}/nihtest-1.9.1 exec %{__python3} -m nihtest "$@"\n' > test-bin/nihtest
chmod 0755 test-bin/nihtest
PATH="$PWD/test-bin:$PATH" %cmake_conf \
  -DBUILD_DOC=ON \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_OSSFUZZ=OFF \
  -DBUILD_REGRESS=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DBUILD_TOOLS=ON \
  -DENABLE_BZIP2=ON \
  -DENABLE_LZMA=ON \
  -DENABLE_OPENSSL=ON \
  -DENABLE_ZSTD=ON \
  -DLIBZIP_DO_INSTALL=ON
%cmake_build

%install
%cmake_install

%check
PATH="$PWD/test-bin:$PATH" PYTHONPATH=%{_builddir}/nihtest-1.9.1 %ctest

%files
%license LICENSE
%doc AUTHORS NEWS.md README.md SECURITY.md THANKS
%{_bindir}/zipcmp
%{_bindir}/zipmerge
%{_bindir}/ziptool
%{_libdir}/libzip.so.5*
%{_mandir}/man1/zip*.1*

%files devel
%license LICENSE
%{_includedir}/zip.h
%{_includedir}/zipconf.h
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/libzip.pc
%{_libdir}/cmake/libzip/
%{_mandir}/man3/*.3*
%{_mandir}/man5/*.5*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.4-1
- Initial openEuler RISC-V package with pinned offline nihtest regression runner.
