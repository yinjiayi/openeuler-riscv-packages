# SPDX-License-Identifier: Apache-2.0
Name:           readline
Version:        8.3
Release:        3%{?dist}
Summary:        Library for interactive command line editing
License:        GPL-3.0-or-later
URL:            https://tiswww.case.edu/php/chet/readline/rltop.html
Source0:        readline-8.3.tar.gz
Source1:        readline83-001
Source2:        readline83-002
Source3:        readline83-003

BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  patch
BuildRequires:  pkgconf-pkg-config

%description
GNU Readline provides command-line editing and history facilities for
interactive applications. This package includes the companion History
library and official patches through patch level 003.

%package devel
Summary:        Development files for GNU Readline
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ncurses-devel

%description devel
Headers, linker names, pkg-config files, manuals, and static API metadata for
building applications with GNU Readline and History.

%prep
%setup -q -n readline-8.3
patch -p0 < %{SOURCE1}
patch -p0 < %{SOURCE2}
patch -p0 < %{SOURCE3}

%build
%configure --disable-static --with-curses
%make_build SHLIB_LIBS=-lncurses

%install
%make_install SHLIB_LIBS=-lncurses
rm -f %{buildroot}%{_libdir}/*.a

%check
%make_build check
%make_build -C examples check
test "$(cat patchlevel)" = 3

%files
%license COPYING
%doc CHANGES NEWS README USAGE
%{_libdir}/libhistory.so.8*
%{_libdir}/libreadline.so.8*

%files devel
%{_includedir}/readline/
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%{_libdir}/pkgconfig/history.pc
%{_libdir}/pkgconfig/readline.pc
%{_mandir}/man3/history.3*
%{_mandir}/man3/readline.3*
%{_infodir}/history.info*
%{_infodir}/readline.info*
%{_infodir}/rluserman.info*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 8.3-3
- Initial openEuler RISC-V package with official patches through 003.
