# SPDX-License-Identifier: Apache-2.0
Name:           watchflower
Version:        5.4
Release:        2%{?dist}
Summary:        A plant monitoring application that reads and plots data from compatible Bluetooth sensors like Xiaomi 'Flower Care' or Parrot 'Flower Power'
License:        GPL-3.0-or-later
URL:            https://github.com/emericg/WatchFlower
Source0:        watchflower-5.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtcharts-devel
BuildRequires:  qt6-qtconnectivity-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel

%description
A plant monitoring application that reads and plots data from compatible Bluetooth sensors like Xiaomi 'Flower Care' or Parrot 'Flower Power'

%prep
%autosetup -n WatchFlower-%{version} -p1

%build
%cmake -S . -B %{_vpath_builddir} \
  -DBUILD_TESTING=ON
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
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4-2
- Match the case-sensitive upstream archive root and configure out of source.
- Declare every Qt 6 development component required by the desktop build.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4-1
- Initial openEuler RISC-V package from the full package inventory.
