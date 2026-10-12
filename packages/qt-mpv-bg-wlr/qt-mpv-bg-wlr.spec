# SPDX-License-Identifier: Apache-2.0
Name:           qt-mpv-bg-wlr
Version:        0.0.3
Release:        1%{?dist}
Summary:        A mpv based video wallpaper program for wlroots based wayland compositors. (Video Dynamic Wallpaper for Linux).
License:        GPL-3.0-or-later
URL:            https://github.com/lisuke/qt-mpv-bg-wlr
Source0:        qt-mpv-bg-wlr-0.0.3.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
A mpv based video wallpaper program for wlroots based wayland compositors. (Video Dynamic Wallpaper for Linux).

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
