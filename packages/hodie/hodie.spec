# SPDX-License-Identifier: Apache-2.0
Name:           hodie
Version:        1.5.0
Release:        1%{?dist}
Summary:        Latin date (1)
License:        MIT
URL:            https://github.com/michiexile/hodie
Source0:        hodie-1.5.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Latin date (1)

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
%doc README
%doc CHANGELOG

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.5.0-1
- Initial openEuler RISC-V package from the full package inventory.
