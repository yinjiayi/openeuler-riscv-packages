# SPDX-License-Identifier: Apache-2.0
Name:           openxr-explorer
Version:        1.7
Release:        1%{?dist}
Summary:        Debug tool for OpenXR developers
License:        MIT
URL:            https://github.com/maluoi/openxr-explorer
Source0:        openxr-explorer-1.7.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Debug tool for OpenXR developers

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.7-1
- Initial openEuler RISC-V package from the full package inventory.
