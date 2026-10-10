# SPDX-License-Identifier: Apache-2.0
Name:           figlet
Version:        2.2.5
Release:        1%{?dist}
Summary:        Render large text banners using FIGlet fonts
License:        BSD-3-Clause
URL:            https://github.com/cmatsuoka/figlet
Source0:        figlet-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
FIGlet renders large text banners from a collection of FIGlet font and
control files. This package includes the upstream font tools and manual pages.

%prep
%autosetup -p1

%build
%make_build \
  CC=%{__cc} LD=%{__cc} \
  CFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" \
  DEFAULTFONTDIR=%{_datadir}/figlet

%install
%make_install \
  prefix=%{_prefix} \
  BINDIR=%{_bindir} MANDIR=%{_mandir} \
  DEFAULTFONTDIR=%{_datadir}/figlet

%check
# Retain all 26 upstream rendering cases and version consistency checks.
%make_build check vercheck DEFAULTFONTDIR=%{_datadir}/figlet

%files
%license LICENSE
%doc CHANGES FAQ README figfont.txt
%{_bindir}/figlet
%{_bindir}/chkfont
%{_bindir}/figlist
%{_bindir}/showfigfonts
%{_datadir}/figlet/
%{_mandir}/man6/figlet.6*
%{_mandir}/man6/chkfont.6*
%{_mandir}/man6/figlist.6*
%{_mandir}/man6/showfigfonts.6*

%changelog
* Tue Sep 29 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2.5-1
- Package the official SHA-256-pinned FIGlet release with all upstream tests.
