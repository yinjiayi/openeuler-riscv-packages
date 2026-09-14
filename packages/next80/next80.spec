# SPDX-License-Identifier: Apache-2.0
Name:           next80
Version:        1.0.0
Release:        1%{?dist}
Summary:        8080, Z80, R800, Z280 and eZ80 assembler/linker toolchain compatible with MACRO-80
License:        MIT
URL:            https://github.com/lvitals/next80
Source0:        next80-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
8080, Z80, R800, Z280 and eZ80 assembler/linker toolchain compatible with MACRO-80

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
