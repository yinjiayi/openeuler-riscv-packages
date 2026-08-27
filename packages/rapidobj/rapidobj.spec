# SPDX-License-Identifier: Apache-2.0
Name:           rapidobj
Version:        1.1
Release:        1%{?dist}
Summary:        A fast, header-only, C++17 library for parsing Wavefront .obj files.
License:        MIT
URL:            https://github.com/guybrush77/rapidobj
Source0:        rapidobj-1.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A fast, header-only, C++17 library for parsing Wavefront .obj files.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1-1
- Initial openEuler RISC-V package from the full package inventory.
