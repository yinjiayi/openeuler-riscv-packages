# SPDX-License-Identifier: Apache-2.0
Name:           aspen
Version:        0.1.0
Release:        1%{?dist}
Summary:        Fast, byte-compatible reimplementation of tree(1) in C (GNU tree 2.3.2)
License:        MIT
URL:            https://github.com/tenseleyFlow/aspen
Source0:        aspen-0.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Fast, byte-compatible reimplementation of tree(1) in C (GNU tree 2.3.2)

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
