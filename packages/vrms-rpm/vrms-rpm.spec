# SPDX-License-Identifier: Apache-2.0
Name:           vrms-rpm
Version:        2.4
Release:        1%{?dist}
Summary:        Report non-free software
License:        GPL-3.0-or-later
URL:            https://github.com/suve/vrms-rpm
Source0:        vrms-rpm-2.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Report non-free software

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
%license LICENCE.txt
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.4-1
- Initial openEuler RISC-V package from the full package inventory.
