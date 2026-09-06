# SPDX-License-Identifier: Apache-2.0
Name:           astrorama-elements
Version:        6.3.4
Release:        1%{?dist}
Summary:        A C++/Python build framework that helps to organize the software into modules which are gathered into projects
License:        LGPL-3.0-or-later
URL:            https://github.com/astrorama/Elements
Source0:        astrorama-elements-6.3.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A C++/Python build framework that helps to organize the software into modules which are gathered into projects

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
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.3.4-1
- Initial openEuler RISC-V package from the full package inventory.
