# SPDX-License-Identifier: Apache-2.0
Name:           contour
Version:        0.6.3.8249
Release:        7%{?dist}
Summary:        Modern C++ Terminal Emulator
License:        Apache-2.0
URL:            https://github.com/contour-terminal/contour
Source0:        contour-0.6.3.8249.tar.gz
Patch0:         0001-find-qt-wayland-private-target-via-public-component.patch
BuildRequires:  cairo-devel
BuildRequires:  catch2-devel >= 3.4.0
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel >= 2.10.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  harfbuzz-devel
BuildRequires:  libssh2-devel
BuildRequires:  libutempter-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-gui
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  wayland-devel

%description
Modern C++ Terminal Emulator

%prep
%autosetup -p1

%build
%cmake -S . -B %{_vpath_builddir} -DCONTOUR_TESTING=ON
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license LICENSE.txt
%doc README.md

%changelog
* Tue Sep 08 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-7
- Allow the complete QEMU build and CTest suite to use a 240-minute package
  budget after the 120-minute budget expired during error-free compilation.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-6
- Allow the complete QEMU build and test suite to use a 120-minute package budget.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-5
- Add the matching Qt 6 private headers required by the exported Wayland private target.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-4
- Load Qt's private Wayland target through the public component exported by openEuler Qt 6.5.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-3
- Add the XKB, Qt 6 Wayland, and Wayland development dependencies required by the Linux GUI build.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-2
- Use the compatible system Freetype provider and enable the upstream CTest suite.
- Declare the platform development dependencies required by the upstream build.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-1
- Initial openEuler RISC-V package from the full package inventory.
