# SPDX-License-Identifier: Apache-2.0
Name:           reflection-cpp
Version:        0.4.0
Release:        1%{?dist}
Summary:        C++ static reflection support library
License:        Apache-2.0
URL:            https://github.com/contour-terminal/reflection-cpp
Source0:        reflection-cpp-0.4.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
C++ static reflection support library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.0-1
- Initial openEuler RISC-V package from the full package inventory.
