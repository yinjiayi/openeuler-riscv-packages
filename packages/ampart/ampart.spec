# SPDX-License-Identifier: Apache-2.0
Name:           ampart
Version:        1.4.1
Release:        1%{?dist}
Summary:        A partition tool to modify Amlogic's proprietary eMMC partition format and FDT
License:        GPL-3.0-or-later
URL:            https://github.com/7Ji/ampart
Source0:        ampart-1.4.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A partition tool to modify Amlogic's proprietary eMMC partition format and FDT

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.1-1
- Initial openEuler RISC-V package from the full package inventory.
