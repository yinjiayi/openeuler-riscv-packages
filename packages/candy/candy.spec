# SPDX-License-Identifier: Apache-2.0
Name:           candy
Version:        6.1.9
Release:        1%{?dist}
Summary:        A tool for creating and managing a virtual network implemented in C++
License:        MIT
URL:            https://github.com/lanthora/candy
Source0:        candy-6.1.9.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A tool for creating and managing a virtual network implemented in C++

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 6.1.9-1
- Initial openEuler RISC-V package from the full package inventory.
