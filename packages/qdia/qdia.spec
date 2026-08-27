# SPDX-License-Identifier: Apache-2.0
Name:           qdia
Version:        0.64
Release:        1%{?dist}
Summary:        Simple schematic/diagram editor with focus on quick diagram generation with high quality graphics, inspired by xcircuit
License:        AGPL-3.0
URL:            https://github.com/sunderme/qdia
Source0:        qdia-0.64.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Simple schematic/diagram editor with focus on quick diagram generation with high quality graphics, inspired by xcircuit

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
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.64-1
- Initial openEuler RISC-V package from the full package inventory.
