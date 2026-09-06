# SPDX-License-Identifier: Apache-2.0
Name:           wtmpdb
Version:        0.76.0
Release:        1%{?dist}
Summary:        Database for recording the last logged in users and system reboots
License:        BSD-2-Clause
URL:            https://github.com/thkukuk/wtmpdb
Source0:        wtmpdb-0.76.0.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  meson
BuildRequires:  ninja-build

%description
Database for recording the last logged in users and system reboots

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
find %{buildroot} \( -type f -o -type l \) -printf '/%%P\n' | LC_ALL=C sort > %{name}.files
test -s %{name}.files

%check
%meson_test

%files -f %{name}.files
%license LICENSE
%doc README.md
%doc NEWS

%changelog
* Wed Aug 26 2026 openEuler RISC-V Maintainers <noreply@example.invalid> - 0.76.0-1
- Initial openEuler RISC-V package from the full package inventory.
