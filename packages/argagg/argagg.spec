# SPDX-License-Identifier: Apache-2.0
Name:           argagg
Version:        0.4.7
Release:        1%{?dist}
Summary:        A simple C++11 command line argument parser
License:        MIT
URL:            https://github.com/vietjtnguyen/argagg
Source0:        argagg-0.4.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A simple C++11 command line argument parser

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
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.4.7-1
- Initial openEuler RISC-V package from the full package inventory.
