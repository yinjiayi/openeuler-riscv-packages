# SPDX-License-Identifier: Apache-2.0
Name:           slang
Version:        2.3.3
Release:        4%{?dist}
Summary:        Embeddable interpreted language and application library
License:        GPL-2.0-or-later
URL:            https://www.jedsoft.org/slang/
Source0:        slang-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  libpng-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  oniguruma-devel
BuildRequires:  pcre-devel
BuildRequires:  pkgconf
BuildRequires:  zlib-devel

%description
S-Lang is an embeddable interpreted language and a C library providing
screen, terminal, string, array, and application-development facilities.
The package also supplies the slsh standalone interpreter and loadable
modules.

%package devel
Summary:        Development files for S-Lang
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconf

%description devel
Headers, pkg-config metadata, and the unversioned linker name for developing
applications against the S-Lang library.

%package help
Summary:        Documentation for S-Lang and slsh
BuildArch:      noarch

%description help
The S-Lang and slsh reference documentation and the slsh manual page.

%prep
%autosetup -p1

%build
%configure \
  --with-readline=slang \
  --with-pcrelib=%{_libdir} \
  --with-pcreinc=%{_includedir} \
  --with-oniglib=%{_libdir} \
  --with-oniginc=%{_includedir} \
  --with-pnglib=%{_libdir} \
  --with-pnginc=%{_includedir} \
  --with-zlib=%{_libdir} \
  --with-zinc=%{_includedir}
%make_build

%install
%make_install

%check
TERM=xterm %make_build check

%files
%license COPYING
%{_bindir}/slsh
%config(noreplace) %{_sysconfdir}/slsh.rc
%{_libdir}/libslang.so.2*
%{_libdir}/slang/
%{_datadir}/slsh/

%files devel
%license COPYING
%{_includedir}/slang.h
%{_includedir}/slcurses.h
%{_libdir}/libslang.so
%{_libdir}/pkgconfig/slang.pc

%files help
%license COPYING
%{_docdir}/slang/
%{_docdir}/slsh/
%{_mandir}/man1/slsh.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.3-4
- Rebuild S-Lang for openEuler RISC-V from Fedora 44 and frozen cross-distribution evidence.
- Preserve the target libslang.so.2 ABI and run the complete upstream test gate.
