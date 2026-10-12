# SPDX-License-Identifier: Apache-2.0
Name:           except-c
Version:        2.1.0
Release:        1%{?dist}
Summary:        This module offers a straightforward macro interface that facilitates seamless exception handling in the C programming language, drawing inspiration from th
License:        MIT
URL:            https://github.com/alecksandr26/except-c
Source0:        except-c-2.1.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
This module offers a straightforward macro interface that facilitates seamless exception handling in the C programming language, drawing inspiration from th

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 2.1.0-1
- Initial openEuler RISC-V package from the full package inventory.
