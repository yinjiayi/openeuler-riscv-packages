# SPDX-License-Identifier: Apache-2.0
Name:           tail-tray
Version:        0.2.34
Release:        3%{?dist}
Summary:        Tailscale tray menu and UI for the KDE Plasma Desktop
License:        GPL-3.0-or-later
URL:            https://github.com/SneWs/tail-tray
Source0:        tail-tray-0.2.34.tar.gz
Patch0:         0001-qt65-translation-setup.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel

%description
Tailscale tray menu and UI for the KDE Plasma Desktop

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
* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.34-3
- Backport translation setup compatible with openEuler's Qt 6.5.

* Fri Aug 28 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.34-2
- Add the OpenGL and Qt 6 development files required by CMake and tests.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.34-1
- Initial openEuler RISC-V package from the full package inventory.
