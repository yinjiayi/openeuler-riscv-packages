# SPDX-License-Identifier: Apache-2.0
Name:           osm-gps-map
Version:        1.2.0
Release:        1%{?dist}
Summary:        Gtk Widget for Displaying OpenStreetMap tiles
License:        GPL-2.0-or-later
URL:            https://github.com/nzjrs/osm-gps-map
Source0:        osm-gps-map-1.2.0.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  make

%description
Gtk Widget for Displaying OpenStreetMap tiles

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
