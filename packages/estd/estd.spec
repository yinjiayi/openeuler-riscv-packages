# SPDX-License-Identifier: Apache-2.0
Name:           estd
Version:        0.6.5
Release:        1%{?dist}
Summary:        Extended C++ library in the style of the standard library
License:        BSD-3-Clause
URL:            https://github.com/fizyr/estd
Source0:        estd-0.6.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Extended C++ library in the style of the standard library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.5-1
- Initial openEuler RISC-V package from the full package inventory.
