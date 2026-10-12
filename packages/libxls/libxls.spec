# SPDX-License-Identifier: Apache-2.0
Name:           libxls
Version:        1.6.3
Release:        1%{?dist}
Summary:        Library and command-line tool for reading Excel XLS files
License:        BSD-2-Clause
URL:            https://github.com/libxls/libxls
Source0:        libxls-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig

%description
libxls reads binary Excel XLS workbooks and includes the xls2csv conversion
tool.

%package devel
Summary:        Development files for libxls
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for programs
using libxls.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libxlsreader.la

%check
%make_build check
./test2_libxls test/files/test2.xls
test -x ./test_cpp
./test_cpp test/files/test2.xls

%files
%license LICENSE
%doc AUTHORS README.md
%{_bindir}/xls2csv
%{_libdir}/libxlsreader.so.8*
%{_mandir}/man1/xls2csv.1*

%files devel
%license LICENSE
%{_includedir}/xls.h
%{_includedir}/libxls/
%{_libdir}/libxlsreader.so
%{_libdir}/pkgconfig/libxls.pc

%changelog
* Mon Sep 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.3-1
- Initial package from the official, SHA-256-pinned libxls release.
