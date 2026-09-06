# SPDX-License-Identifier: Apache-2.0
Name:           qschematic
Version:        3.0.3
Release:        1%{?dist}
Summary:        A library that allows creating diagrams such as flowcharts or even proper engineering schematics within a Qt application
License:        MIT
URL:            https://github.com/simulton/QSchematic
Source0:        qschematic-3.0.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A library that allows creating diagrams such as flowcharts or even proper engineering schematics within a Qt application

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING=ON
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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.3-1
- Initial openEuler RISC-V package from the full package inventory.
