# SPDX-License-Identifier: Apache-2.0
Name:           nxpp
Version:        1.0.21
Release:        1%{?dist}
Summary:        Header-only C++20 graph utilities on top of Boost Graph Library
License:        MIT
URL:            https://github.com/Mik1810/nxpp
Source0:        nxpp-1.0.21.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Header-only C++20 graph utilities on top of Boost Graph Library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.21-1
- Initial openEuler RISC-V package from the full package inventory.
