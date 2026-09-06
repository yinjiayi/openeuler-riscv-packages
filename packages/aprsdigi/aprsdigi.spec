# SPDX-License-Identifier: Apache-2.0
Name:           aprsdigi
Version:        3.11.0
Release:        1%{?dist}
Summary:        a linux amateur radio APRS digipeater
License:        GPL-2.0-or-later
URL:            https://github.com/n2ygk/aprsdigi
Source0:        aprsdigi-3.11.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
a linux amateur radio APRS digipeater

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
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.11.0-1
- Initial openEuler RISC-V package from the full package inventory.
