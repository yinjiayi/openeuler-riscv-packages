# SPDX-License-Identifier: Apache-2.0
Name:           libpal
Version:        0.9.8
Release:        1%{?dist}
Summary:        Positional Astronomy Library
License:        LGPL-3.0-or-later
URL:            https://github.com/Starlink/pal
Source0:        libpal-0.9.8.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Positional Astronomy Library

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
%license COPYING.LESSER
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.9.8-1
- Initial openEuler RISC-V package from the full package inventory.
