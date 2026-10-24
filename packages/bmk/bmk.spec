# SPDX-License-Identifier: Apache-2.0
Name:           bmk
Version:        0.2
Release:        1%{?dist}
Summary:        successor to make(1) with support for subdirectories
License:        ISC
URL:            https://github.com/realchonk/bmk
Source0:        bmk-0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
successor to make(1) with support for subdirectories

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.2-1
- Initial openEuler RISC-V package from the full package inventory.
