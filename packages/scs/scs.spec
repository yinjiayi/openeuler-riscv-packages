# SPDX-License-Identifier: Apache-2.0
Name:           scs
Version:        3.2.6
Release:        1%{?dist}
Summary:        Numerical package for solving large-scale convex cone problems
License:        MIT
URL:            https://github.com/cvxgrp/scs
Source0:        scs-3.2.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Numerical package for solving large-scale convex cone problems

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
%license LICENSE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.2.6-1
- Initial openEuler RISC-V package from the full package inventory.
