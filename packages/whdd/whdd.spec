# SPDX-License-Identifier: Apache-2.0
Name:           whdd
Version:        3.1
Release:        1%{?dist}
Summary:        Diagnostic and recovery tool for block devices (near to replace MHDD for Linux)
License:        GPL-3.0-or-later
URL:            https://github.com/whdd/whdd
Source0:        whdd-3.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Diagnostic and recovery tool for block devices (near to replace MHDD for Linux)

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
%license COPYING
%license LICENSE
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.1-1
- Initial openEuler RISC-V package from the full package inventory.
