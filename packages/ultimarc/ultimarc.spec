# SPDX-License-Identifier: Apache-2.0
Name:           ultimarc
Version:        1.2.0
Release:        1%{?dist}
Summary:        Library and command line utility to configure Ultimarc boards
License:        GPL-2.0-or-later
URL:            https://github.com/katie-snow/Ultimarc-linux
Source0:        ultimarc-1.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Library and command line utility to configure Ultimarc boards

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
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
