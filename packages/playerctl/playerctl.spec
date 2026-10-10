# SPDX-License-Identifier: Apache-2.0
Name:           playerctl
Version:        2.4.1
Release:        1%{?dist}
Summary:        mpris media player controller and lib for spotify, vlc, audacious, bmp, xmms2, and others.
License:        LGPL-3.0-or-later
URL:            https://github.com/altdesktop/playerctl
Source0:        playerctl-2.4.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
mpris media player controller and lib for spotify, vlc, audacious, bmp, xmms2, and others.

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

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
