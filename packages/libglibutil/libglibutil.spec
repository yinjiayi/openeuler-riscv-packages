# SPDX-License-Identifier: Apache-2.0
Name:           libglibutil
Version:        1.0.82
Release:        1%{?dist}
Summary:        Library of glib utilities
License:        BSD-3-Clause
URL:            https://github.com/sailfishos/libglibutil
Source0:        libglibutil-1.0.82.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
Library of glib utilities

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
%doc README

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 1.0.82-1
- Initial openEuler RISC-V package from the full package inventory.
