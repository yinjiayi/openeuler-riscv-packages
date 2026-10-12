# SPDX-License-Identifier: Apache-2.0
Name:           archium
Version:        1.10.4
Release:        1%{?dist}
Summary:        Fast & Easy Package Management for Arch Linux
License:        BSD-3-Clause
URL:            https://github.com/keircn/archium
Source0:        archium-1.10.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Fast & Easy Package Management for Arch Linux

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.10.4-1
- Initial openEuler RISC-V package from the full package inventory.
