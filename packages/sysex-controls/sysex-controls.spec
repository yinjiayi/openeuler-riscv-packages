# SPDX-License-Identifier: Apache-2.0
Name:           sysex-controls
Version:        0.2.28
Release:        1%{?dist}
Summary:        Linux alternative to the MIDI Control Center software
License:        GPL-3.0-or-later
URL:            https://github.com/soyersoyer/sysex-controls
Source0:        sysex-controls-0.2.28.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Linux alternative to the MIDI Control Center software

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.28-1
- Initial openEuler RISC-V package from the full package inventory.
