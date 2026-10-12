# SPDX-License-Identifier: Apache-2.0
Name:           biolibc
Version:        0.2.7
Release:        1%{?dist}
Summary:        High-performance, memory-efficient bioinformatics library
License:        BSD-2-Clause
URL:            https://github.com/auerlab/biolibc
Source0:        biolibc-0.2.7.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
High-performance, memory-efficient bioinformatics library

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2.7-1
- Initial openEuler RISC-V package from the full package inventory.
