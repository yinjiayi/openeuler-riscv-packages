# SPDX-License-Identifier: Apache-2.0
Name:           masscan
Version:        1.3.2
Release:        1%{?dist}
Summary:        TCP port scanner, spews SYN packets asynchronously, scanning entire Internet in under 5 minutes
License:        AGPL-3.0
URL:            https://github.com/robertdavidgraham/masscan
Source0:        masscan-1.3.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
TCP port scanner, spews SYN packets asynchronously, scanning entire Internet in under 5 minutes

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.3.2-1
- Initial openEuler RISC-V package from the full package inventory.
