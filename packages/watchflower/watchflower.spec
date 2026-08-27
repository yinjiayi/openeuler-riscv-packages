# SPDX-License-Identifier: Apache-2.0
Name:           watchflower
Version:        5.4
Release:        1%{?dist}
Summary:        A plant monitoring application that reads and plots data from compatible Bluetooth sensors like Xiaomi 'Flower Care' or Parrot 'Flower Power'
License:        GPL-3.0-or-later
URL:            https://github.com/emericg/WatchFlower
Source0:        watchflower-5.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A plant monitoring application that reads and plots data from compatible Bluetooth sensors like Xiaomi 'Flower Care' or Parrot 'Flower Power'

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.4-1
- Initial openEuler RISC-V package from the full package inventory.
