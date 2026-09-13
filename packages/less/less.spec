# SPDX-License-Identifier: Apache-2.0
Name:           less
Version:        704
Release:        1%{?dist}
Summary:        Terminal file pager
License:        (GPL-3.0-only OR BSD-2-Clause) AND GPL-2.0-or-later
URL:            https://www.greenwoodsoftware.com/less/
Source0:        less-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  perl
BuildRequires:  pcre2-devel

%description
Less is a terminal pager that displays text one screen at a time and supports
backward movement, searching, filtering, and large files.

%prep
%autosetup -p1

%build
%configure --disable-silent-rules --with-regex=pcre2
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING LICENSE
%doc INSTALL NEWS README
%{_bindir}/less
%{_bindir}/lesskey
%{_libexecdir}/lessecho
%{_libexecdir}/less-osc8-open
%{_mandir}/man1/less.1*
%{_mandir}/man1/lesskey.1*
%{_mandir}/man1/lessecho.1*

%changelog
* Wed Aug 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 704-1
- Initial openEuler RISC-V package from frozen cross-distribution and upstream evidence.
