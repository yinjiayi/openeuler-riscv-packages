# SPDX-License-Identifier: Apache-2.0
Name:           bgpq3
Version:        0.1.38
Release:        1%{?dist}
Summary:        bgp filtering automation for Cisco and Juniper routers
License:        BSD-2-Clause
URL:            https://github.com/snar/bgpq3
Source0:        bgpq3-0.1.38.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
bgp filtering automation for Cisco and Juniper routers

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
%license COPYRIGHT
%doc README.md

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.1.38-1
- Initial openEuler RISC-V package from the full package inventory.
