# SPDX-License-Identifier: Apache-2.0
Name:           alias-manager
Version:        2.3.1
Release:        1%{?dist}
Summary:        Lightweight CLI tool for managing shell aliases
License:        MIT
URL:            https://github.com/kazetachinuu/alias_manager
Source0:        alias-manager-2.3.1.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Lightweight CLI tool for managing shell aliases

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.3.1-1
- Initial openEuler RISC-V package from the full package inventory.
