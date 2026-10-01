# SPDX-License-Identifier: Apache-2.0
Name:           ds5-edge-relay
Version:        2.1.0
Release:        1%{?dist}
Summary:        Qt6 GUI relay daemon for DualSense Edge — presents it as standard DualSense to fix Proton/Steam compatibility, with button remapping, macro recorder and qui
License:        MIT
URL:            https://github.com/Follen22/ds5-edge-relay
Source0:        ds5-edge-relay-2.1.0.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Qt6 GUI relay daemon for DualSense Edge — presents it as standard DualSense to fix Proton/Steam compatibility, with button remapping, macro recorder and qui

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
