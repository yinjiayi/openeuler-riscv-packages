# SPDX-License-Identifier: Apache-2.0
Name:           openosc
Version:        1.0.6
Release:        1%{?dist}
Summary:        Open Object Size Check Library
License:        Apache-2.0
URL:            https://github.com/cisco/openosc
Source0:        openosc-1.0.6.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Open Object Size Check Library

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
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.6-1
- Initial openEuler RISC-V package from the full package inventory.
