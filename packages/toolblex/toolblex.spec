# SPDX-License-Identifier: Apache-2.0
Name:           toolblex
Version:        0.17
Release:        1%{?dist}
Summary:        A Bluetooth Low Energy device scanner and analyzer
License:        GPL-3.0-or-later
URL:            https://github.com/emericg/toolBLEx
Source0:        toolblex-0.17.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A Bluetooth Low Energy device scanner and analyzer

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
%license LICENSE.md
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.17-1
- Initial openEuler RISC-V package from the full package inventory.
