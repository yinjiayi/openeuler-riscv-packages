# SPDX-License-Identifier: Apache-2.0
Name:           tcptrack
Version:        1.4.3
Release:        1%{?dist}
Summary:        A sniffer which displays information about TCP connections it sees on a network interface
License:        LGPL-2.1-or-later
URL:            https://github.com/bchretien/tcptrack
Source0:        tcptrack-1.4.3.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A sniffer which displays information about TCP connections it sees on a network interface

%prep
%autosetup -p1

%build
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
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
