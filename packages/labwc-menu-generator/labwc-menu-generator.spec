# SPDX-License-Identifier: Apache-2.0
Name:           labwc-menu-generator
Version:        0.1.0
Release:        1%{?dist}
Summary:        Menu generator for labwc
License:        GPL-2.0-or-later
URL:            https://github.com/labwc/labwc-menu-generator
Source0:        labwc-menu-generator-0.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Menu generator for labwc

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
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the GLib development dependency required by Meson.
