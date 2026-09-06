# SPDX-License-Identifier: Apache-2.0
Name:           libpaper
Version:        2.3.0
Release:        1%{?dist}
Summary:        Library and utilities for handling paper sizes
License:        LGPL-2.1-or-later AND GPL-2.0-only AND GPL-3.0-or-later AND MIT AND LicenseRef-Public-Domain
URL:            https://github.com/rrthomas/libpaper
Source0:        libpaper-2.3.0.tar.gz

BuildRequires:  gcc
BuildRequires:  help2man
BuildRequires:  make
BuildRequires:  perl

%description
libpaper provides a paper-size database, a C library for querying it, and
paper and paperconf command-line utilities.

%package devel
Summary:        Development files for libpaper
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header and unversioned library link for developing applications with libpaper.

%prep
%autosetup -p1

%build
%configure --enable-relocatable --disable-static
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libpaper.la

%check
%make_build check

%files
%license COPYING COPYING-GPL-3 COPYING-MIT
%doc AUTHORS ChangeLog README.md
%config(noreplace) %{_sysconfdir}/paperspecs
%{_bindir}/paper
%{_bindir}/paperconf
%{_libdir}/libpaper.so.2*
%{_mandir}/man1/paper.1*
%{_mandir}/man5/paperspecs.5*

%files devel
%license COPYING COPYING-GPL-3 COPYING-MIT
%{_includedir}/paper.h
%{_libdir}/libpaper.so

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.8-1
- Initial openEuler RISC-V package.
