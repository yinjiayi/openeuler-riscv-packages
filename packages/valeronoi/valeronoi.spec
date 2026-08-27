# SPDX-License-Identifier: Apache-2.0
Name:           valeronoi
Version:        0.2.1
Release:        1%{?dist}
Summary:        WiFi mapping companion app for Valetudo
License:        GPL-3.0-or-later
URL:            https://github.com/ccoors/Valeronoi
Source0:        valeronoi-0.2.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
WiFi mapping companion app for Valetudo

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
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.1-1
- Initial openEuler RISC-V package from the full package inventory.
