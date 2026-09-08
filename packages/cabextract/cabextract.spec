# SPDX-License-Identifier: Apache-2.0
Name:           cabextract
Version:        1.11
Release:        1%{?dist}
Summary:        Extract Microsoft cabinet files
License:        GPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.0-or-later
URL:            https://www.cabextract.org.uk/
Source0:        cabextract-1.11.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%description
cabextract is a command-line tool for listing, testing, and extracting
Microsoft cabinet archives, including cabinets embedded in executables.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%check
%make_build check

%files
%license COPYING mspack/mspack.h getopt.c
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/cabextract
%{_mandir}/man1/cabextract.1*

%changelog
* Sat Aug 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11-1
- Initial openEuler RISC-V package.
