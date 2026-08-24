# SPDX-License-Identifier: Apache-2.0
Name:           gawk
Version:        5.4.1
Release:        1%{?dist}
Summary:        GNU implementation of the AWK programming language
License:        GPL-3.0-or-later
URL:            https://www.gnu.org/software/gawk/
Source0:        gawk-5.4.1.tar.xz

Provides:       /usr/bin/awk
Provides:       /usr/bin/gawk
BuildRequires:  gcc
BuildRequires:  libsigsegv-devel
BuildRequires:  make
BuildRequires:  mpfr-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  readline-devel

%description
GNU awk is a pattern scanning and processing language for text files.

%package devel
Summary:        Development header for gawk extensions
Requires:       gawk%{?_isa} = %{version}-%{release}

%description devel
The gawk API header used to build dynamically loaded extensions.

%prep
%autosetup -p1

%build
%configure --disable-static --disable-pma --with-mpfr --with-readline
%make_build

%install
%make_install
rm -f %{buildroot}%{_infodir}/dir
ln -s gawk.1 %{buildroot}%{_mandir}/man1/awk.1

%check
%make_build check

%files
%license COPYING
%doc NEWS README POSIX.STD README_d/README.multibyte
%{_bindir}/awk
%{_bindir}/gawk
%{_bindir}/gawk-*
%{_bindir}/gawkbug
%{_libdir}/libgawk.so.*
%{_libexecdir}/awk/
%{_datadir}/awk/
%{_mandir}/man1/awk.1*
%{_mandir}/man1/gawk*.1*
%{_mandir}/man3/*awk*.3*
%{_infodir}/gawk*.info*
%{_datadir}/locale/*/LC_MESSAGES/gawk.mo

%files devel
%{_includedir}/gawkapi.h
%{_libdir}/libgawk.so

%changelog
* Sun Aug 16 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4.1-1
- Package gawk with MPFR/readline support and the complete upstream test suite.
