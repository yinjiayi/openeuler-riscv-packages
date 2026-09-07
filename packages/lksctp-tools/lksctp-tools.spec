# SPDX-License-Identifier: Apache-2.0
Name:           lksctp-tools
Version:        1.0.21
Release:        2%{?dist}
Summary:        An implementation of the SCTP protocol
License:        GPL-2.0-or-later
URL:            https://github.com/sctp/lksctp-tools
Source0:        lksctp-tools-1.0.21.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
An implementation of the SCTP protocol

%prep
%autosetup -p1

%build
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) ! -path '%{buildroot}%{_mandir}/*' -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%license COPYING.lib
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.21-2
- List compressed manual pages with RPM path macros.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.21-1
- Initial openEuler RISC-V package from the full package inventory.
