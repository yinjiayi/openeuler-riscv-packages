# SPDX-License-Identifier: Apache-2.0
Name:           osgxr
Version:        0.5.6
Release:        1%{?dist}
Summary:        Library to integrate OpenXR into OpenSceneGraph applications
License:        LGPL-2.1-or-later
URL:            https://github.com/amalon/osgXR
Source0:        osgxr-0.5.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Library to integrate OpenXR into OpenSceneGraph applications

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.5.6-1
- Initial openEuler RISC-V package from the full package inventory.
