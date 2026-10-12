# SPDX-License-Identifier: Apache-2.0
Name:           nqptp
Version:        1.2.8
Release:        1%{?dist}
Summary:        A daemon that monitors timing data from PTP clocks
License:        GPL-2.0-or-later
URL:            https://github.com/mikebrady/nqptp
Source0:        nqptp-1.2.8.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A daemon that monitors timing data from PTP clocks

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
%doc README
%doc README.md
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.8-1
- Initial openEuler RISC-V package from the full package inventory.
