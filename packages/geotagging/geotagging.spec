# SPDX-License-Identifier: Apache-2.0
Name:           geotagging
Version:        0.7.4
Release:        1%{?dist}
Summary:        Photography geotagging tool to synchronize photos with gps track log (GPX)
License:        GPL-3.0-or-later
URL:            https://github.com/jmlich/geotagging
Source0:        geotagging-0.7.4.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Photography geotagging tool to synchronize photos with gps track log (GPX)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.7.4-1
- Initial openEuler RISC-V package from the full package inventory.
