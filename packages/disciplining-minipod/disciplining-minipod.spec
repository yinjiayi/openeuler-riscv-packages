# SPDX-License-Identifier: Apache-2.0
Name:           disciplining-minipod
Version:        3.8.4
Release:        1%{?dist}
Summary:        Disciplining algorithm for Atomic Reference Time Card
License:        LGPL-2.1-or-later
URL:            https://github.com/Orolia2s/disciplining-minipod
Source0:        disciplining-minipod-3.8.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Disciplining algorithm for Atomic Reference Time Card

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.8.4-1
- Initial openEuler RISC-V package from the full package inventory.
