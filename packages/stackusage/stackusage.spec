# SPDX-License-Identifier: Apache-2.0
Name:           stackusage
Version:        1.21
Release:        1%{?dist}
Summary:        Measure stack usage in Linux applications
License:        BSD-3-Clause
URL:            https://github.com/d99kris/stackusage
Source0:        stackusage-1.21.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Measure stack usage in Linux applications

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.21-1
- Initial openEuler RISC-V package from the full package inventory.
