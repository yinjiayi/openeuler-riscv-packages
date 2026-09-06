# SPDX-License-Identifier: Apache-2.0
Name:           loveshaderconverter
Version:        0.1
Release:        1%{?dist}
Summary:        Converts the GLSL used in the Shader Toy to a version of GLSL that can be used by LÖVE, with custom calls for lua
License:        MIT
URL:            https://github.com/tsteinholz/LoveShaderConverter
Source0:        loveshaderconverter-0.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
Converts the GLSL used in the Shader Toy to a version of GLSL that can be used by LÖVE, with custom calls for lua

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1-1
- Initial openEuler RISC-V package from the full package inventory.
