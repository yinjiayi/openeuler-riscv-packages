# SPDX-License-Identifier: Apache-2.0
Name:           thermofun
Version:        0.6.0
Release:        1%{?dist}
Summary:        Library for calculating standard state thermodynamic properties
License:        LGPL-2.1-or-later
URL:            https://github.com/thermohub/thermofun
Source0:        thermofun-0.6.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Library for calculating standard state thermodynamic properties

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.0-1
- Initial openEuler RISC-V package from the full package inventory.
