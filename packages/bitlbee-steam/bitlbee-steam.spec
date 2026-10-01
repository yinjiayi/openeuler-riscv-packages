# SPDX-License-Identifier: Apache-2.0
Name:           bitlbee-steam
Version:        1.4.2
Release:        1%{?dist}
Summary:        Steam protocol plugin for BitlBee
License:        GPL-2.0-or-later
URL:            https://github.com/bitlbee/bitlbee-steam
Source0:        bitlbee-steam-1.4.2.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Steam protocol plugin for BitlBee

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
%doc NEWS
%doc AUTHORS
%doc ChangeLog

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-1
- Initial openEuler RISC-V package from the full package inventory.
