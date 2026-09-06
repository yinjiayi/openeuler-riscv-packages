# SPDX-License-Identifier: Apache-2.0
Name:           picotool
Version:        2.3.0
Release:        1%{?dist}
Summary:        Tool for inspecting RP2040 binaries and interacting with RP2040 devices.
License:        BSD-3-Clause
URL:            https://github.com/raspberrypi/picotool
Source0:        picotool-2.3.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Tool for inspecting RP2040 binaries and interacting with RP2040 devices.

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
%license LICENSE.TXT
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
