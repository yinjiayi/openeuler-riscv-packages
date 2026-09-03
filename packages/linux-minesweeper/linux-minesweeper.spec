# SPDX-License-Identifier: Apache-2.0
Name:           linux-minesweeper
Version:        2.0.1
Release:        1%{?dist}
Summary:        A faithful recreation of the Windows 7 Minesweeper
License:        GPL-3.0-or-later
URL:            https://github.com/actuallyaridan/linux-minesweeper
Source0:        linux-minesweeper-2.0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtmultimedia-devel

%description
A faithful recreation of the Windows 7 Minesweeper

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.0.1-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the Qt 6 development dependencies required by CMake.
