# SPDX-License-Identifier: Apache-2.0
Name:           libopnmidi
Version:        1.6.1
Release:        1%{?dist}
Summary:        A software MIDI synthesizer library with OPN2 (YM2612) emulation
License:        LGPL-3.0-or-later
URL:            https://github.com/Wohlstand/libOPNMIDI
Source0:        libopnmidi-1.6.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A software MIDI synthesizer library with OPN2 (YM2612) emulation

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
%license LICENSE.GPL-3.txt
%license LICENSE.LGPL-2.1.txt
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.6.1-1
- Initial openEuler RISC-V package from the full package inventory.
