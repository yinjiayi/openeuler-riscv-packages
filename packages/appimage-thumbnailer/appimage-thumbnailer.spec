# SPDX-License-Identifier: Apache-2.0
Name:           appimage-thumbnailer
Version:        4.1.1
Release:        1%{?dist}
Summary:        Generates AppImage thumbnails for Linux desktops
License:        MIT
URL:            https://github.com/kem-a/appimage-thumbnailer
Source0:        appimage-thumbnailer-4.1.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Generates AppImage thumbnails for Linux desktops

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.1.1-1
- Initial openEuler RISC-V package from the full package inventory.
