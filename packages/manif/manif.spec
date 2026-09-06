# SPDX-License-Identifier: Apache-2.0
Name:           manif
Version:        0.0.5
Release:        1%{?dist}
Summary:        A small C++11 header-only library for Lie theory.
License:        MIT
URL:            https://github.com/artivis/manif
Source0:        manif-0.0.5.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A small C++11 header-only library for Lie theory.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.5-1
- Initial openEuler RISC-V package from the full package inventory.
