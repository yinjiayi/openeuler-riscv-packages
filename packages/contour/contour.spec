# SPDX-License-Identifier: Apache-2.0
Name:           contour
Version:        0.6.3.8249
Release:        2%{?dist}
Summary:        Modern C++ Terminal Emulator
License:        Apache-2.0
URL:            https://github.com/contour-terminal/contour
Source0:        contour-0.6.3.8249.tar.gz
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
BuildRequires:  make
BuildRequires:  pkgconf
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-gui
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtmultimedia-devel

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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-2
- Use the compatible system Freetype provider and enable the upstream CTest suite.
- Declare the platform development dependencies required by the upstream build.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.3.8249-1
- Initial openEuler RISC-V package from the full package inventory.
