# SPDX-License-Identifier: Apache-2.0
Name:           boxed-cpp
Version:        1.4.3
Release:        1%{?dist}
Summary:        Small header-only library for easing primitive type boxing in C++
License:        Apache-2.0
URL:            https://github.com/contour-terminal/boxed-cpp
Source0:        boxed-cpp-1.4.3.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Small header-only library for easing primitive type boxing in C++

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.3-1
- Initial openEuler RISC-V package from the full package inventory.
