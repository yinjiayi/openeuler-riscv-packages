# SPDX-License-Identifier: Apache-2.0
Name:           wallpaperengine-gui
Version:        1.2.0
Release:        1%{?dist}
Summary:        GUI for linux-wallpaperengine
License:        MIT
URL:            https://github.com/MikiDevLog/wallpaperengine-gui
Source0:        wallpaperengine-gui-1.2.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel

%description
GUI for linux-wallpaperengine

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.2.0-1
- Initial openEuler RISC-V package from the full package inventory.
- Add the Qt 6 development files required by CMake.
