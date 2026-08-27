# SPDX-License-Identifier: Apache-2.0
Name:           deepin-grand-search
Version:        5.5.11
Release:        1%{?dist}
Summary:        System-wide desktop search for DDE
License:        GPL-3.0-or-later
URL:            https://github.com/linuxdeepin/dde-grand-search
Source0:        deepin-grand-search-5.5.11.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
System-wide desktop search for DDE

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.5.11-1
- Initial openEuler RISC-V package from the full package inventory.
