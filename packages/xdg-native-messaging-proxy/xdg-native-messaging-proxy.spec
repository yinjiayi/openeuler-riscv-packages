# SPDX-License-Identifier: Apache-2.0
Name:           xdg-native-messaging-proxy
Version:        0.1.0
Release:        1%{?dist}
Summary:        Allow sandboxed applications to find and use native messaging hosts outside of the sandbox via dbus.
License:        LGPL-2.1-or-later
URL:            https://github.com/flatpak/xdg-native-messaging-proxy
Source0:        xdg-native-messaging-proxy-0.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Allow sandboxed applications to find and use native messaging hosts outside of the sandbox via dbus.

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
%doc NEWS.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
