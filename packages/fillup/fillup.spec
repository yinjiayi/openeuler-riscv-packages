# SPDX-License-Identifier: Apache-2.0
Name:           fillup
Version:        1.42
Release:        1%{?dist}
Summary:        Tool for Merging Config Files
License:        GPL-2.0-or-later
URL:            https://github.com/openSUSE/fillup
Source0:        fillup-1.42.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Tool for Merging Config Files

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.42-1
- Initial openEuler RISC-V package from the full package inventory.
