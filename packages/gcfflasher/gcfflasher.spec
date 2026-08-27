# SPDX-License-Identifier: Apache-2.0
Name:           gcfflasher
Version:        4.11.0
Release:        1%{?dist}
Summary:        Tool to program the firmware of dresden elektronik's Zigbee products.
License:        BSD-3-Clause
URL:            https://github.com/dresden-elektronik/gcfflasher
Source0:        gcfflasher-4.11.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Tool to program the firmware of dresden elektronik's Zigbee products.

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.11.0-1
- Initial openEuler RISC-V package from the full package inventory.
