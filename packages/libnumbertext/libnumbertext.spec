# SPDX-License-Identifier: Apache-2.0
Name:           libnumbertext
Version:        1.0.11
Release:        1%{?dist}
Summary:        Number-to-text conversion library
License:        (LGPL-3.0-or-later OR BSD-3-Clause) AND (LGPL-3.0-or-later OR CC-BY-SA-3.0)
URL:            https://github.com/Numbertext/libnumbertext
Source0:        libnumbertext-%{version}.tar.xz

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  diffutils
BuildRequires:  gawk
BuildRequires:  gcc-c++
BuildRequires:  grep
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  sed

%description
libnumbertext converts numbers and monetary values into text using Soros
language modules. It includes the spellout command-line client and language
data for more than forty languages.

%package devel
Summary:        Development files for libnumbertext
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned shared-library link for
developing C++ applications with libnumbertext.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libnumbertext-1.0.la

%check
%make_build check

%files
%license COPYING
%doc AUTHORS ChangeLog README.md
%{_bindir}/spellout
%{_datadir}/libnumbertext/
%{_libdir}/libnumbertext-1.0.so.0*

%files devel
%license COPYING
%{_includedir}/libnumbertext/
%{_libdir}/libnumbertext-1.0.so
%{_libdir}/pkgconfig/libnumbertext.pc

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.11-1
- Initial openEuler RISC-V package with the complete upstream test suite.
