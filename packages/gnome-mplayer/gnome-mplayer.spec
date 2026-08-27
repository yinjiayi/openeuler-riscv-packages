# SPDX-License-Identifier: Apache-2.0
Name:           gnome-mplayer
Version:        1.0.9
Release:        1%{?dist}
Summary:        GTK/Gnome interface around MPlayer
License:        GPL-2.0-or-later
URL:            https://github.com/kdekorte/gnome-mplayer
Source0:        gnome-mplayer-1.0.9.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
GTK/Gnome interface around MPlayer

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.9-1
- Initial openEuler RISC-V package from the full package inventory.
