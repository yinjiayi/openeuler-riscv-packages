# SPDX-License-Identifier: Apache-2.0
Name:           rtorrent
Version:        0.16.19
Release:        1%{?dist}
Summary:        Console-based BitTorrent client
License:        GPL-2.0-or-later
URL:            https://github.com/rakshasa/rtorrent
Source0:        rtorrent-0.16.19.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

%description
Console-based BitTorrent client

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
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.16.19-1
- Initial openEuler RISC-V package from the full package inventory.
