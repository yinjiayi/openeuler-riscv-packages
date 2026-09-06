# SPDX-License-Identifier: Apache-2.0
Name:           switchtec
Version:        4.3
Release:        1%{?dist}
Summary:        Userspace code for the Microsemi PCIe switch
License:        MIT
URL:            https://github.com/Microsemi/switchtec-user
Source0:        switchtec-4.3.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Userspace code for the Microsemi PCIe switch

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 4.3-1
- Initial openEuler RISC-V package from the full package inventory.
