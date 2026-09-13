# SPDX-License-Identifier: Apache-2.0
Name:           cunit
Version:        2.1.3
Release:        1%{?dist}
Summary:        Unit testing framework for C
License:        LGPL-2.0-only
URL:            https://cunit.sourceforge.net/
Source0:        CUnit-2.1-3.tar.bz2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config

%description
CUnit is a portable unit testing framework for C programs. It provides a
shared library with automated, basic, and console interfaces.

%package libs
Summary:        Shared CUnit library

%description libs
This package contains the CUnit shared library used by test programs.

%package devel
Summary:        Development files for CUnit
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       pkgconf-pkg-config

%description devel
This package contains CUnit headers, the unversioned linker name, and
pkg-config metadata for developing C unit tests.

%package help
Summary:        Documentation and XML support files for CUnit
BuildArch:      noarch

%description help
This package contains the CUnit manual page, HTML documentation, and XML
DTD/XSL support files.

%prep
%autosetup -n CUnit-2.1-3 -p1

%build
autoreconf -fi
%configure \
  --disable-static \
  --enable-automated \
  --enable-basic \
  --enable-console \
  --disable-curses \
  --disable-examples \
  --enable-test
%make_build

%install
%make_install docdir=%{_docdir}/%{name}
rm -f %{buildroot}%{_libdir}/*.la
# The upstream install target places its architecture-specific internal test
# executable under the shared-data directory; it is already exercised in %check.
rm -f %{buildroot}%{_datadir}/CUnit/Test/test_cunit
rmdir %{buildroot}%{_datadir}/CUnit/Test

%check
%make_build check
./CUnit/Sources/Test/test_cunit

%files
%license COPYING

%files libs
%{_libdir}/libcunit.so.1*

%files devel
%{_includedir}/CUnit/
%{_libdir}/libcunit.so
%{_libdir}/pkgconfig/cunit.pc

%files help
%doc README AUTHORS NEWS ChangeLog
%{_docdir}/%{name}/
%{_prefix}/doc/CUnit/headers/
%{_mandir}/man3/CUnit.3*
%{_datadir}/CUnit/

%changelog
* Thu Aug 20 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.3-1
- Initial CUnit package for openEuler RISC-V.
