# SPDX-License-Identifier: Apache-2.0
Name:           luau
Version:        0.733
Release:        1%{?dist}
Summary:        A fast, small, safe, gradually typed embeddable scripting language derived from Lua
License:        MIT
URL:            https://github.com/luau-lang/luau
Source0:        luau-0.733.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make

%description
A fast, small, safe, gradually typed embeddable scripting language derived from Lua

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.733-1
- Initial openEuler RISC-V package from the full package inventory.
