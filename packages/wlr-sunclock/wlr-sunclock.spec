# SPDX-License-Identifier: Apache-2.0
Name:           wlr-sunclock
Version:        1.2.1
Release:        3%{?dist}
Summary:        Displays a sunclock desktop widget using the layer shell protocol
License:        LGPL-3.0-or-later
URL:            https://github.com/sentriz/wlr-sunclock
Source0:        wlr-sunclock-1.2.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  gtk4-devel
BuildRequires:  pkgconfig(gtk4-layer-shell-0)

%description
Displays a sunclock desktop widget using the layer shell protocol

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
%license LICENCE
%doc README.md

%changelog
* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-3
- Declare the gtk4-layer-shell pkg-config interface required by Meson.

* Thu Sep 03 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-2
- Add the GTK 4 development dependency required by Meson configuration.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
