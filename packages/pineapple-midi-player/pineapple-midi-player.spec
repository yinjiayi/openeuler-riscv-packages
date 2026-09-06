# SPDX-License-Identifier: Apache-2.0
Name:           pineapple-midi-player
Version:        2.0.0
Release:        1%{?dist}
Summary:        Simple SoundFont MIDI Player
License:        MIT
URL:            https://github.com/BLumia/pineapple-midi-player
Source0:        pineapple-midi-player-2.0.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Simple SoundFont MIDI Player

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
