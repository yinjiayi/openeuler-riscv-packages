# SPDX-License-Identifier: Apache-2.0
Name:           image-gtk
Version:        23.5
Release:        1%{?dist}
Summary:        A simple, fast and elegant image viewer program
License:        GPL-3.0-or-later
URL:            https://github.com/vl-nix/image-gtk
Source0:        image-gtk-23.5.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A simple, fast and elegant image viewer program

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
%license License


%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 23.5-1
- Initial openEuler RISC-V package from the full package inventory.
