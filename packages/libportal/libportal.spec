# SPDX-License-Identifier: Apache-2.0
Name:           libportal
Version:        0.10.0
Release:        1%{?dist}
Summary:        GIO-style async APIs for most Flatpak portals
License:        LGPL-3.0-or-later
URL:            https://github.com/flatpak/libportal
Source0:        libportal-0.10.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
GIO-style async APIs for most Flatpak portals

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.10.0-1
- Initial openEuler RISC-V package from the full package inventory.
