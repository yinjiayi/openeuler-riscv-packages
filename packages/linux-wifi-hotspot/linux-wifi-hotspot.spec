# SPDX-License-Identifier: Apache-2.0
Name:           linux-wifi-hotspot
Version:        4.7.2
Release:        1%{?dist}
Summary:        Feature-rich wifi hotspot creator
License:        BSD-2-Clause
URL:            https://github.com/lakinduakash/linux-wifi-hotspot
Source0:        linux-wifi-hotspot-4.7.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Feature-rich wifi hotspot creator

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.7.2-1
- Initial openEuler RISC-V package from the full package inventory.
