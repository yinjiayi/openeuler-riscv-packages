# SPDX-License-Identifier: Apache-2.0
Name:           libi2cd
Version:        1.0.3
Release:        1%{?dist}
Summary:        C library for interacting with linux I2C devices
License:        LGPL-2.1-or-later
URL:            https://github.com/sstallion/libi2cd
Source0:        libi2cd-1.0.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
C library for interacting with linux I2C devices

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
%doc README.md
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
