# SPDX-License-Identifier: Apache-2.0
Name:           inkaur
Version:        0.1.0
Release:        1%{?dist}
Summary:        A simple, lightweight, and fast AUR helper written in C
License:        MIT
URL:            https://github.com/lvitals/inkaur
Source0:        inkaur-0.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A simple, lightweight, and fast AUR helper written in C

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
