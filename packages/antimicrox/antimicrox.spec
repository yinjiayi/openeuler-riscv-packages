# SPDX-License-Identifier: Apache-2.0
Name:           antimicrox
Version:        3.6.1
Release:        1%{?dist}
Summary:        Graphical program used to map keyboard buttons & mouse controls to a gamepad
License:        GPL-3.0-or-later
URL:            https://github.com/AntiMicroX/antimicrox
Source0:        antimicrox-3.6.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Graphical program used to map keyboard buttons & mouse controls to a gamepad

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.6.1-1
- Initial openEuler RISC-V package from the full package inventory.
