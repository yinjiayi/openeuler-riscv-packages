# SPDX-License-Identifier: Apache-2.0
Name:           vsgxchange
Version:        1.1.13
Release:        1%{?dist}
Summary:        Utility library for converting data+materials to/from VulkanSceneGraph
License:        MIT
URL:            https://github.com/vsg-dev/vsgXchange
Source0:        vsgxchange-1.1.13.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Utility library for converting data+materials to/from VulkanSceneGraph

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
%license LICENSE.md
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.13-1
- Initial openEuler RISC-V package from the full package inventory.
