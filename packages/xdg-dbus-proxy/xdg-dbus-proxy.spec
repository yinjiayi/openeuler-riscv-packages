# SPDX-License-Identifier: Apache-2.0
Name:           xdg-dbus-proxy
Version:        0.1.7
Release:        1%{?dist}
Summary:        Filtering proxy for D-Bus connections
License:        LGPL-2.1-or-later
URL:            https://github.com/flatpak/xdg-dbus-proxy
Source0:        xdg-dbus-proxy-0.1.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Filtering proxy for D-Bus connections

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.7-1
- Initial openEuler RISC-V package from the full package inventory.
