# SPDX-License-Identifier: Apache-2.0
Name:           gmime3
Version:        3.2.15
Release:        1%{?dist}
Summary:        A C/C++ MIME creation and parser library with support for S/MIME, PGP, and Unix mbox spools
License:        LGPL-2.1-or-later
URL:            https://github.com/jstedfast/gmime
Source0:        gmime3-3.2.15.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A C/C++ MIME creation and parser library with support for S/MIME, PGP, and Unix mbox spools

%prep
%autosetup -p1

%build
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
%license LICENSE
%doc README.md
%doc NEWS
%doc AUTHORS

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.15-1
- Initial openEuler RISC-V package from the full package inventory.
