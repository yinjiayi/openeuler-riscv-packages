# SPDX-License-Identifier: Apache-2.0
Name:           avra
Version:        1.4.2
Release:        1%{?dist}
Summary:        Assembler for the Atmel AVR microcontroller family
License:        GPL-2.0-or-later
URL:            https://github.com/hsoft/avra
Source0:        avra-1.4.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Assembler for the Atmel AVR microcontroller family

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
%license COPYING
%doc README.md
%doc AUTHORS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.4.2-1
- Initial openEuler RISC-V package from the full package inventory.
