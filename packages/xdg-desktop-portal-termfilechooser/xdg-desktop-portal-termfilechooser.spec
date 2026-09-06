# SPDX-License-Identifier: Apache-2.0
Name:           xdg-desktop-portal-termfilechooser
Version:        1.4.3
Release:        1%{?dist}
Summary:        xdg-desktop-portal backend for your favorite terminal file chooser (hunkyburrito fork)
License:        MIT
URL:            https://github.com/hunkyburrito/xdg-desktop-portal-termfilechooser
Source0:        xdg-desktop-portal-termfilechooser-1.4.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
xdg-desktop-portal backend for your favorite terminal file chooser (hunkyburrito fork)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
