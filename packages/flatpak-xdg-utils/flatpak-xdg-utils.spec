# SPDX-License-Identifier: Apache-2.0
Name:           flatpak-xdg-utils
Version:        1.0.6
Release:        1%{?dist}
Summary:        Simple portal-based commandline tools for use inside flatpak sandboxes
License:        LGPL-2.1-or-later
URL:            https://github.com/flatpak/flatpak-xdg-utils
Source0:        flatpak-xdg-utils-1.0.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Simple portal-based commandline tools for use inside flatpak sandboxes

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
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
