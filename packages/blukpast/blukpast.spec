# SPDX-License-Identifier: Apache-2.0
Name:           blukpast
Version:        1.0.6
Release:        1%{?dist}
Summary:        Lightweight Vulkan graphics library in C — pipelines, descriptors, buffers, textures, GLTF/OBJ/PLY/STL loaders
License:        LGPL-2.1-or-later
URL:            https://github.com/wypifu/blukpast
Source0:        blukpast-1.0.6.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
Lightweight Vulkan graphics library in C — pipelines, descriptors, buffers, textures, GLTF/OBJ/PLY/STL loaders

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
