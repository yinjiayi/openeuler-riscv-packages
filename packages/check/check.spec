# SPDX-License-Identifier: Apache-2.0
Name:           check
Version:        0.15.2
Release:        1%{?dist}
Summary:        Unit testing framework for C
License:        LGPL-2.1-or-later
URL:            https://libcheck.github.io/check
Source0:        check-%{version}.tar.gz

BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  make

%description
Check is a unit testing framework for C. It supports isolated test execution,
fixtures, multiple output formats, and test-suite composition.

%package devel
Summary:        Development files for Check
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers, pkg-config metadata, and the unversioned library link for developing
C test suites with Check.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --disable-build-docs \
  --disable-subunit
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -delete

%check
%make_build check

%files
%license COPYING.LESSER
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/checkmk
%{_libdir}/libcheck.so.0*
%{_mandir}/man1/checkmk.1*

%files devel
%license COPYING.LESSER
%{_includedir}/check.h
%{_includedir}/check_stdint.h
%{_libdir}/libcheck.so
%{_libdir}/pkgconfig/check.pc
%{_datadir}/aclocal/check.m4

%changelog
* Tue Aug 11 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.15.2-1
- Initial openEuler RISC-V package based on Fedora 44 and corroborating release evidence.
