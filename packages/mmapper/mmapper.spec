# SPDX-License-Identifier: Apache-2.0
Name:           mmapper
Version:        25.07.0
Release:        1%{?dist}
Summary:        MMapper2 is a MUD (Multi-User Dungeon) mapper especially written for the MUD MUME
License:        GPL-2.0-or-later
URL:            https://github.com/MUME/MMapper
Source0:        mmapper-25.07.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
MMapper2 is a MUD (Multi-User Dungeon) mapper especially written for the MUD MUME

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
%license COPYING.txt
%doc README.md
%doc NEWS.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 25.07.0-1
- Initial openEuler RISC-V package from the full package inventory.
