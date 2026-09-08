# SPDX-License-Identifier: Apache-2.0
Name:           libmaxminddb
Version:        1.13.3
Release:        1%{?dist}
Summary:        Library for reading MaxMind DB files
License:        Apache-2.0
URL:            https://maxmind.github.io/libmaxminddb
Source0:        libmaxminddb-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  perl

%description
libmaxminddb provides a C API and command-line lookup utility for databases in
the MaxMind DB binary format.

%package devel
Summary:        Development files for libmaxminddb
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, API manual pages, and the unversioned shared
library link for developing software with libmaxminddb.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --enable-binaries \
  --enable-tests
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license LICENSE
%doc AUTHORS Changes.md README.md
%{_bindir}/mmdblookup
%{_libdir}/libmaxminddb.so.0*
%{_mandir}/man1/mmdblookup.1*

%files devel
%license LICENSE
%{_includedir}/maxminddb.h
%{_includedir}/maxminddb_config.h
%{_libdir}/libmaxminddb.so
%{_libdir}/pkgconfig/libmaxminddb.pc
%{_mandir}/man3/*.3*

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.13.3-1
- Initial openEuler RISC-V package based on cross-distribution release evidence.
