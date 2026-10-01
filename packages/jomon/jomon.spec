# SPDX-License-Identifier: Apache-2.0
Name:           jomon
Version:        0.6.4
Release:        1%{?dist}
Summary:        Network forensics and sniffer tool
License:        MIT
URL:            https://github.com/jo-lund/jomon
Source0:        jomon-0.6.4.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Network forensics and sniffer tool

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.6.4-1
- Initial openEuler RISC-V package from the full package inventory.
