# SPDX-License-Identifier: Apache-2.0
Name:           deepin-lianliankan
Version:        6.0.11
Release:        3%{?dist}
Summary:        An easy-to-play puzzle game with cute interface and countdown timer
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/deepin-lianliankan
Source0:        deepin-lianliankan-6.0.11.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libxkbcommon-devel
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtmultimedia-devel

%description
An easy-to-play puzzle game with cute interface and countdown timer

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.11-3
- Add the XKB and Qt Multimedia development dependencies.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.11-2
- Add the Qt 6 base development dependency required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.0.11-1
- Initial openEuler RISC-V package from the full package inventory.
