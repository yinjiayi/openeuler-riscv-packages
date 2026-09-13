# SPDX-License-Identifier: Apache-2.0
Name:           deepin-font-manager
Version:        6.5.16
Release:        4%{?dist}
Summary:        A font management tool for Deepin desktop
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/deepin-font-manager
Source0:        deepin-font-manager-6.5.16.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libxkbcommon-devel
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qttools-devel

%description
A font management tool for Deepin desktop

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.5.16-4
- Add the Qt 6 LinguistTools development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.5.16-3
- Add the XKB and Qt 6 SVG development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.5.16-2
- Add the Qt 6 base development files required by CMake.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.5.16-1
- Initial openEuler RISC-V package from the full package inventory.
