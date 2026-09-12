# SPDX-License-Identifier: Apache-2.0
Name:           qschematic
Version:        3.0.3
Release:        5%{?dist}
Summary:        A library that allows creating diagrams such as flowcharts or even proper engineering schematics within a Qt application
License:        MIT AND Zlib
URL:            https://github.com/simulton/QSchematic
Source0:        qschematic-3.0.3.tar.gz
Source1:        gpds-1.10.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  qt6-qtbase-devel

%description
A library that allows creating diagrams such as flowcharts or even proper engineering schematics within a Qt application

%prep
%autosetup -n QSchematic-%{version} -p1 -a 1
# Retain distinct upstream notices for the bundled serialization dependency.
cp -p gpds-1.10.0/license.txt gpds-LICENSE.txt
cp -p gpds-1.10.0/gpds/3rdparty/miniyaml/LICENSE miniyaml-LICENSE.txt
cp -p gpds-1.10.0/gpds/3rdparty/tinyxml2/LICENSE.txt tinyxml2-LICENSE.txt

%build
%cmake -S . -B %{_vpath_builddir} -DBUILD_TESTING=ON \
  -DFETCHCONTENT_FULLY_DISCONNECTED=ON \
  -DFETCHCONTENT_SOURCE_DIR_GPDS="$PWD/gpds-1.10.0"
%cmake_build

%install
%cmake_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
ctest --test-dir %{_vpath_builddir} --output-on-failure

%files -f %{name}.files
%license license.txt
%license gpds-LICENSE.txt miniyaml-LICENSE.txt tinyxml2-LICENSE.txt


%changelog
* Sat Sep 12 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-5
- Pin the GPDS 1.10.0 source archive and use its verified local source tree.
- Include GPDS, MiniYAML and TinyXML-2 license notices.
- Allow 120 minutes after dependency installation reduced the compilation budget.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-4
- Allow 90 minutes for QEMU compilation, tests, and RPM finalization.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-3
- Add the Qt 6 development dependency and use one explicit CMake build directory.

* Mon Sep 07 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-2
- Match the exact case-sensitive root of the verified upstream source archive.

* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
