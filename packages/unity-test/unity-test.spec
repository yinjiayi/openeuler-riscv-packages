# SPDX-License-Identifier: Apache-2.0
Name:           unity-test
Version:        2.6.1
Release:        1%{?dist}
Summary:        Simple unit testing for C
License:        MIT
URL:            https://github.com/throwtheswitch/unity
Source0:        unity-test-2.6.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Simple unit testing for C

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.6.1-1
- Initial openEuler RISC-V package from the full package inventory.
