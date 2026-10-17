# SPDX-License-Identifier: Apache-2.0
Name:           pspg
Version:        5.8.16
Release:        1%{?dist}
Summary:        Tabular data pager designed to be used with psql
License:        BSD-2-Clause
URL:            https://github.com/okbob/pspg
Source0:        pspg-5.8.16.tar.gz
BuildRequires:  gcc
BuildRequires:  libpq-devel
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel

%description
Tabular data pager designed to be used with psql

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
./pspg --version

%files -f %{name}.files
%license LICENSE
%doc README.md

%changelog
* Thu Aug 27 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 5.8.16-1
- Initial openEuler RISC-V package from the full package inventory.
- Add terminal, readline, and PostgreSQL development dependencies.
- Run the upstream executable check because this release has no check target.
