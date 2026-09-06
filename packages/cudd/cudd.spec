# SPDX-License-Identifier: Apache-2.0
Name:           cudd
Version:        3.0.0
Release:        1%{?dist}
Summary:        A package for the manipulation of Binary Decision Diagrams (BDDs) and similar structures
License:        BSD-3-Clause
URL:            https://github.com/ivmai/cudd
Source0:        cudd-3.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A package for the manipulation of Binary Decision Diagrams (BDDs) and similar structures

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%make_build check

%files -f %{name}.files
%license LICENSE
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 3.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
