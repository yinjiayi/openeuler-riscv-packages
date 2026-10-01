# SPDX-License-Identifier: Apache-2.0
Name:           arp-scan
Version:        1.10.0
Release:        1%{?dist}
Summary:        A tool that uses ARP to discover and fingerprint IP hosts on the local network
License:        GPL-3.0-or-later
URL:            https://github.com/royhills/arp-scan
Source0:        arp-scan-1.10.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
A tool that uses ARP to discover and fingerprint IP hosts on the local network

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
%doc AUTHORS
%doc ChangeLog

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10.0-1
- Initial openEuler RISC-V package from the full package inventory.
