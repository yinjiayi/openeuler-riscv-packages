# SPDX-License-Identifier: Apache-2.0
Name:           osc2midi
Version:        0.2.5
Release:        1%{?dist}
Summary:        A highly flexible and configurable OSC to JACK MIDI (and back) bridge
License:        GPL-3.0-or-later
URL:            https://github.com/ssj71/osc2midi
Source0:        osc2midi-0.2.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A highly flexible and configurable OSC to JACK MIDI (and back) bridge

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.5-1
- Initial openEuler RISC-V package from the full package inventory.
