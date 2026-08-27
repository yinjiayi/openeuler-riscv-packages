# SPDX-License-Identifier: Apache-2.0
Name:           angie-mod-njs
Version:        1.0.0
Release:        1%{?dist}
Summary:        nginScript module for angie
License:        BSD-2-Clause
URL:            https://github.com/nginx/njs
Source0:        angie-mod-njs-1.0.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
nginScript module for angie

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
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.0-1
- Initial openEuler RISC-V package from the full package inventory.
