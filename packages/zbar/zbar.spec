# SPDX-License-Identifier: Apache-2.0
Name:           zbar
Version:        0.23.93
Release:        1%{?dist}
Summary:        Application and library for reading bar codes from various sources
License:        LGPL-2.1-or-later
URL:            https://github.com/mchehab/zbar
Source0:        zbar-0.23.93.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Application and library for reading bar codes from various sources

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
%license LICENSE.md
%doc README.md
%doc NEWS.md
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.23.93-1
- Initial openEuler RISC-V package from the full package inventory.
