# SPDX-License-Identifier: Apache-2.0
Name:           cpp-peglib
Version:        1.15.1
Release:        1%{?dist}
Summary:        A single file C++ header-only PEG (Parsing Expression Grammars) library
License:        MIT
URL:            https://github.com/yhirose/cpp-peglib
Source0:        cpp-peglib-1.15.1.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A single file C++ header-only PEG (Parsing Expression Grammars) library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.15.1-1
- Initial openEuler RISC-V package from the full package inventory.
