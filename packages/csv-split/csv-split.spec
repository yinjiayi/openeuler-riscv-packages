# SPDX-License-Identifier: Apache-2.0
Name:           csv-split
Version:        0.0.2
Release:        1%{?dist}
Summary:        A command line tool for splitting CSV files
License:        GPL-3.0-or-later
URL:            https://github.com/mifrandir/csv-split
Source0:        csv-split-0.0.2.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
A command line tool for splitting CSV files

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
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.0.2-1
- Initial openEuler RISC-V package from the full package inventory.
