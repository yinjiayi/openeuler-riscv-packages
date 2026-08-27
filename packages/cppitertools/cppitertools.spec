# SPDX-License-Identifier: Apache-2.0
Name:           cppitertools
Version:        2.2
Release:        1%{?dist}
Summary:        Python itertools and builtin iteration functions for C++17
License:        BSD-2-Clause
URL:            https://github.com/ryanhaining/cppitertools
Source0:        cppitertools-2.2.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Python itertools and builtin iteration functions for C++17

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.2-1
- Initial openEuler RISC-V package from the full package inventory.
