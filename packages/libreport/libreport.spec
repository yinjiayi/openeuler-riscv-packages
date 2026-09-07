# SPDX-License-Identifier: Apache-2.0
Name:           libreport
Version:        2.17.15
Release:        5%{?dist}
Summary:        Generic library for reporting various problems
License:        GPL-2.0-or-later
URL:            https://github.com/abrt/libreport
Source0:        libreport-2.17.15.tar.gz
BuildRequires:  asciidoc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  augeas
BuildRequires:  augeas-devel
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  glib2-devel >= 2.43.4
BuildRequires:  glibc-all-langpacks
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  json-c-devel
BuildRequires:  libarchive-devel
BuildRequires:  libcurl-devel
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  newt-devel
BuildRequires:  python3-devel
BuildRequires:  satyr-devel >= 0.38
BuildRequires:  systemd-devel
BuildRequires:  xmlrpc-c-devel
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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-5
- Add the target dependencies required by the default-enabled libreport features.
- Add the locale data used by the upstream test suite.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-4
- Add the asciidoc and xmlto documentation tools required by configure.ac.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-3
- Generate the version input required by configure.ac from the RPM version.
- Add intltool so autoreconf can expand IT_PROG_INTLTOOL.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-2
- Add the gettext-devel provider required by autoreconf for autopoint.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.17.15-1
- Initial openEuler RISC-V package from the full package inventory.
