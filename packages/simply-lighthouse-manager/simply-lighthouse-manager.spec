# SPDX-License-Identifier: Apache-2.0
Name:           simply-lighthouse-manager
Version:        1.1.4
Release:        1%{?dist}
Summary:        Manage SteamVR base station (lighthouse) power via Bluetooth LE - fork of openvr-lighthouse-manager-linux
License:        GPL-3.0-or-later
URL:            https://github.com/SimplyJustJessie/simply-lighthouse-manager
Source0:        simply-lighthouse-manager-1.1.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Manage SteamVR base station (lighthouse) power via Bluetooth LE - fork of openvr-lighthouse-manager-linux

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.4-1
- Initial openEuler RISC-V package from the full package inventory.
