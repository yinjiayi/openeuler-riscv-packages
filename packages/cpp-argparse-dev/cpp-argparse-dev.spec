# SPDX-License-Identifier: Apache-2.0
Name:           cpp-argparse-dev
Version:        1.11.0
Release:        1%{?dist}
Summary:        Python-like argument parser for C++ projects
License:        MIT
URL:            https://github.com/rue-ryuzaki/argparse
Source0:        cpp-argparse-dev-1.11.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Python-like argument parser for C++ projects

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.11.0-1
- Initial openEuler RISC-V package from the full package inventory.
