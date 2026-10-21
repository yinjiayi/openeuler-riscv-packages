# SPDX-License-Identifier: Apache-2.0
Name:           unibilium
Version:        2.1.4
Release:        1%{?dist}
Summary:        Terminfo parsing library
License:        LGPL-3.0-or-later
URL:            https://github.com/neovim/unibilium
Source0:        v2.1.4.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-Test-Harness

%description
unibilium is a small C library for reading and manipulating terminfo database
entries without depending on ncurses.

%package devel
Summary:        Development files for unibilium
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The unibilium header, pkg-config metadata, API manual pages, and unversioned
library link for developing terminal applications.

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a

%check
%make_build test

%files
%license LICENSE LGPLv3
%doc Changes README.md
%{_libdir}/libunibilium.so.4*

%files devel
%license LICENSE LGPLv3
%{_includedir}/unibilium.h
%{_libdir}/libunibilium.so
%{_libdir}/pkgconfig/unibilium.pc
%{_mandir}/man3/unibi*.3*

%changelog
* Mon Aug 10 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.2-1
- Initial openEuler RISC-V package with full upstream Perl test harness.
