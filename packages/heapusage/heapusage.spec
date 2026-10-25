# SPDX-License-Identifier: Apache-2.0
Name:           heapusage
Version:        2.36
Release:        1%{?dist}
Summary:        Find memory leaks in Linux applications
License:        BSD-3-Clause
URL:            https://github.com/d99kris/heapusage
Source0:        heapusage-2.36.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Find memory leaks in Linux applications

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.36-1
- Initial openEuler RISC-V package from the full package inventory.
