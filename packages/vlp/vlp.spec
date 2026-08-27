# SPDX-License-Identifier: Apache-2.0
Name:           vlp
Version:        0.1.2
Release:        1%{?dist}
Summary:        A cli tool that parses /var/log/pacman.log and shows installed packages, sync commands, and upgrades
License:        GPL-3.0-or-later
URL:            https://github.com/vani-tty1/vlp
Source0:        vlp-0.1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A cli tool that parses /var/log/pacman.log and shows installed packages, sync commands, and upgrades

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license COPYING
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
