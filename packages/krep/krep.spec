# SPDX-License-Identifier: Apache-2.0
Name:           krep
Version:        1.1.2
Release:        1%{?dist}
Summary:        fast text search tool with advanced algorithms, SIMD acceleration, multi-threading, and regex support
License:        BSD-2-Clause
URL:            https://github.com/davidesantangelo/krep
Source0:        krep-1.1.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
fast text search tool with advanced algorithms, SIMD acceleration, multi-threading, and regex support

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_prefix}
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build test

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.1.2-1
- Initial openEuler RISC-V package from the full package inventory.
