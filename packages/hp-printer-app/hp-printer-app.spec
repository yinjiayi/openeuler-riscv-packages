# SPDX-License-Identifier: Apache-2.0
Name:           hp-printer-app
Version:        1.3.0
Release:        1%{?dist}
Summary:        Example printer application for HP PCL printers using PAPPL.
License:        Apache-2.0
URL:            https://github.com/michaelrsweet/hp-printer-app
Source0:        hp-printer-app-1.3.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Example printer application for HP PCL printers using PAPPL.

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.0-1
- Initial openEuler RISC-V package from the full package inventory.
