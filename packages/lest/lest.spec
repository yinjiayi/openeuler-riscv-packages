# SPDX-License-Identifier: Apache-2.0
Name:           lest
Version:        1.37.0
Release:        1%{?dist}
Summary:        Tiny C++11 test framework
License:        BSL-1.0
URL:            https://github.com/martinmoene/lest
Source0:        lest-1.37.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Tiny C++11 test framework

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.37.0-1
- Initial openEuler RISC-V package from the full package inventory.
