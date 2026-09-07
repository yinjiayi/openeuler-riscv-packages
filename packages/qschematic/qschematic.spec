# SPDX-License-Identifier: Apache-2.0
Name:           qschematic
Version:        3.0.3
Release:        3%{?dist}
Summary:        A library that allows creating diagrams such as flowcharts or even proper engineering schematics within a Qt application
License:        MIT
URL:            https://github.com/simulton/QSchematic
Source0:        qschematic-3.0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel

%description
A library that allows creating diagrams such as flowcharts or even proper engineering schematics within a Qt application

%prep
%autosetup -n QSchematic-%{version} -p1

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
%license license.txt


%changelog
* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-3
- Add the Qt 6 development dependency and use one explicit CMake build directory.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-2
- Match the exact case-sensitive root of the verified upstream source archive.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
