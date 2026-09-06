# SPDX-License-Identifier: Apache-2.0
Name:           bitlbee-discord
Version:        0.4.3
Release:        1%{?dist}
Summary:        Bitlbee plugin for Discord
License:        GPL-2.0-or-later
URL:            https://github.com/sm00th/bitlbee-discord
Source0:        bitlbee-discord-0.4.3.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Bitlbee plugin for Discord

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
%license LICENSE
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
