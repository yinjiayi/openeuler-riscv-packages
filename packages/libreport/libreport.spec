# SPDX-License-Identifier: Apache-2.0
Name:           libreport
Version:        2.17.15
Release:        4%{?dist}
Summary:        Generic library for reporting various problems
License:        GPL-2.0-or-later
URL:            https://github.com/abrt/libreport
Source0:        libreport-2.17.15.tar.gz
BuildRequires:  asciidoc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  xmlto

%description
Generic library for reporting various problems

%prep
%autosetup -p1

%build
printf '%s' '%{version}' > libreport-version
autoreconf -fi
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-4
- Add the asciidoc and xmlto documentation tools required by configure.ac.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-3
- Generate the version input required by configure.ac from the RPM version.
- Add intltool so autoreconf can expand IT_PROG_INTLTOOL.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-2
- Add the gettext-devel provider required by autoreconf for autopoint.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-1
- Initial openEuler RISC-V package from the full package inventory.
